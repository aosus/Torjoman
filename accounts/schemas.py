from django.shortcuts import get_object_or_404
from pydantic import EmailStr
from ninja import ModelSchema, Schema, Field
from .utils import User
from datetime import time
from .errors import *
from typing import Optional


class UserSchema(ModelSchema):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    username: str = Field(..., min_length=5, max_length=50)
    send_time: time
    number_of_words: int = Field(6, gt=0, le=10)

    class Config:
        model = User
        model_fields = ["id", "first_name", "last_name", "email", "username"]

    def resolve_send_time(self, obj: User):
        return obj.profile.send_time

    def resolve_number_of_words(self, obj: User):
        return obj.profile.number_of_words


class UserCreateSchema(ModelSchema):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    username: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)
    send_time: time
    number_of_words: int = Field(6, gt=0, le=10)

    class Config:
        model = User
        model_fields = ["first_name", "last_name", "username", "email", "password"]

    def to_model(self) -> User:
        if (
            User.objects.filter(username=self.username).exists()
            or User.objects.filter(email=self.email).exists()
        ):
            raise AlreadyExistError()
        user = User(
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            email=self.email,
        )
        user.set_password(self.password)
        user.save()
        return user


class UserUpdateSchema(ModelSchema):
    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    send_time: Optional[time] = None
    number_of_words: Optional[int] = Field(None, gt=0, le=10)

    class Config:
        model = User
        model_fields = ["first_name", "last_name"]

    def to_model(self, username) -> User:
        user = get_object_or_404(User, username=username)
        if self.first_name:
            user.first_name = self.first_name
        if self.last_name:
            user.last_name = self.last_name
        if self.send_time:
            user.profile.send_time = self.send_time
        if self.number_of_words:
            user.profile.number_of_words = self.number_of_words
        user.save()
        return user


class UserLoginSchema(ModelSchema):
    username: str = Field(..., min_length=5, max_length=50)
    password: str = Field(..., min_length=8, max_length=50)

    class Config:
        model = User
        model_fields = ["username", "password"]


class TokensListSchema(Schema):
    access: str
    refresh: str


class EmailSchema(Schema):
    email: EmailStr


class ChangePasswordSchema(Schema):
    username: str = Field(..., min_length=5, max_length=50)
    old_password: str = Field(..., min_length=8, max_length=50)
    new_password: str = Field(..., min_length=8, max_length=50)
