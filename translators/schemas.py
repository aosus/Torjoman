from typing import List
from uuid import UUID
from ninja import ModelSchema, Schema, Field
from .models import (Translator as TranslatorModel)

class Error(Schema):
  message: str

class TranslatorRegister(ModelSchema):
  platform: str
  class Config:
    model = TranslatorModel
    model_exclude = ['id']
  

class TranslatorLogin(Schema):
  uuid: UUID
  platform: str



class Translator(ModelSchema):
  class Config:
    model = TranslatorModel
    model_exclude = ['id']