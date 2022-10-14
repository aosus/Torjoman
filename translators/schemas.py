from typing import List
from uuid import UUID

from ninja import Field, ModelSchema, Schema

from .models import Translator as TranslatorModel


class TranslatorRegister(ModelSchema):
    platform: str

    class Config:
        model = TranslatorModel
        model_exclude = ["id"]
    
    def to_model(self) -> TranslatorModel:
        return TranslatorModel.objects.create(
            name=self.name,
            number_of_words=self.number_of_words,
            send_time=self.send_time,
        )


class TranslatorLogin(ModelSchema):
    platform: str

    class Config:
        model = TranslatorModel
        model_fields = ["uuid"]


class Translator(ModelSchema):
    class Config:
        model = TranslatorModel
        model_exclude = ["id"]
