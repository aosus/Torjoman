import random
from ninja_extra import api_controller, ControllerBase, route
from .utils import User, create_token, refresh_access
from django.shortcuts import get_object_or_404
from .schemas import *
from .errors import *


@api_controller("accounts/")
class AccountsController(ControllerBase):
    @route.get("", response={200: UserSchema})
    def get_me(self, request):
        return request.auth

    @route.post("", auth=None)
    def create_user(self, payload: UserCreateSchema) -> UserSchema:
        user = payload.to_model()
        return 200, user

    @route.post("update", response={200: UserSchema})
    def update_user(self, request, payload: UserUpdateSchema):
        user = payload.to_model(request.auth.username)
        return 200, user

    @route.post("login", auth=None, )
    def login(self, payload: UserLoginSchema) -> UserSchema:
        user = get_object_or_404(User, username=payload.username)
        if user.check_password(payload.password):
            return 200, user
        else:
            raise IncorrectPasswordError()

    @route.post("refresh/{refresh_token}", response={200: TokensListSchema})
    def refresh_tokens(self, refresh_token: str):
        return refresh_access(refresh_token)

    @route.post("change-password", response={200: TokensListSchema})
    def change_password(self, payload: ChangePasswordSchema):
        u = get_object_or_404(User, email=payload.email)
        if u.check_password(payload.current_password):
            u.set_password(payload.new_password)
            u.save()
            return 200, create_token(u.pk)
        else:
            raise IncorrectPasswordError()
