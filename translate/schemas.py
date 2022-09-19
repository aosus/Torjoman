from typing import List
from ninja import ModelSchema, Schema, Field
from .models import Word as WordModel


class WordIn(Schema):
  uuid: str
  word: str
  translate: str

class Word(ModelSchema):
  translates: List[str] = Field(..., alias='get_all_translates')
  class Config:
    model = WordModel
    model_fields = ['word']