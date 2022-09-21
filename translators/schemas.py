from typing import List
from uuid import UUID

from ninja import Field, ModelSchema, Schema

from .models import Translator as TranslatorModel


class TranslatorRegister(ModelSchema):
    platform: str

    class Config:
        model = TranslatorModel
        model_exclude = ["id"]


class TranslatorLogin(ModelSchema):
    platform: str

    class Config:
        model = TranslatorModel
        model_fields = ["uuid"]


class Translator(ModelSchema):
    class Config:
        model = TranslatorModel
        model_exclude = ["id"]
