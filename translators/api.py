from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router

from . import schemas
from .models import Platform, Translator

router = Router()


@router.post("/register", response={200: schemas.Translator})
def register(request, payload: schemas.TranslatorRegister):
    platforms = Platform.get_all_platforms()
    if payload.platform not in platforms:
        return (422,)
    translator = payload.to_model()
    translator.save()
    platform = platforms[payload.platform]
    platform.translators.add(translator)
    platform.save()
    return 200, translator


@router.post("/login", response={200: schemas.Translator})
def login(request, payload: schemas.TranslatorLogin):
    translator = get_object_or_404(Translator, uuid=payload.uuid)
    platforms = Platform.get_all_platforms()
    if payload.platform not in platforms.keys():
        return (422,)
    platform = platforms[payload.platform]
    platform.translators.add(translator)
    platform.save()
    return 200, translator
