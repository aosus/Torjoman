from uuid import UUID

from ninja import Field, ModelSchema, Schema

from .models import SourceTranslation, UserTranslation, Word


class WordIn(ModelSchema):
    by: UUID
    translation: str

    class Config:
        model = Word
        model_fields = ["word"]


class Word(ModelSchema):
    translations: list[str] = Field(..., alias="get_source_translations")

    class Config:
        model = Word
        model_fields = ["word"]
