from django.shortcuts import get_object_or_404
from ninja import ModelSchema, Schema, Field
from .models import Project, Section, Sentence, Translation
from django.contrib.auth.models import User
from accounts.errors import AlreadyExistError
from .utils import normalize_translation, get_close_match
from django.db.models import Count

class OwnerSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ["id", "first_name"]


class ProjectSchema(ModelSchema):
    owner: OwnerSchema

    class Config:
        model = Project
        model_fields = ["id", "owner", "name", "created_at"]


class ProjectCreateSchema(ModelSchema):
    class Config:
        model = Project
        model_fields = ["name"]

    def to_model(self, owner) -> Project:
        if Project.objects.filter(name=self.name, owner=owner):
            raise AlreadyExistError()
        project = Project.objects.create(name=self.name, owner=owner)
        return project


class ProjectUpdateSchema(ModelSchema):
    new_name: str = Field(..., min_length=1, max_length=250)

    class Config:
        model = Project
        model_fields = ["id"]

    def to_model(self, owner) -> Project:
        project = get_object_or_404(Project, pk=self.id)
        project.name = self.new_name
        project.save()
        return project


# Sections


class SectionSchema(ModelSchema):
    class Config:
        model = Section
        model_fields = ["id", "project", "name", "created_at"]


class SectionCreateSchema(ModelSchema):
    class Config:
        model = Section
        model_fields = ["project", "name"]

    def to_model(self) -> Project:
        project = get_object_or_404(Project, pk=self.project)
        if Section.objects.filter(name=self.name, project=project):
            raise AlreadyExistError()
        section = Section.objects.create(name=self.name, project=project)
        return section


class SectionUpdateSchema(ModelSchema):
    new_name: str = Field(..., min_length=1, max_length=250)

    class Config:
        model = Section
        model_fields = ["id"]

    def to_model(self) -> Section:
        section = get_object_or_404(Section, pk=self.id)
        section.name = self.new_name
        section.save()
        return section


# Sections


class SentenceSchema(ModelSchema):
    class Config:
        model = Sentence
        model_fields = ["id", "section", "sentence", "created_at"]

class SentenceFullSchema(ModelSchema):
    translations: list[str]
    class Config:
        model = Sentence
        model_fields = ["id", "section", "sentence", "created_at"]
    
    def resolve_translations(self, obj: Sentence):
        return Translation.objects.filter(sentence=obj).annotate(votes=Count("voters")).order_by("-votes").values_list('translation', flat=True)


class SentenceCreateSchema(ModelSchema):
    class Config:
        model = Sentence
        model_fields = ["section", "sentence"]

    def to_model(self) -> Sentence:
        section = get_object_or_404(Section, pk=self.section)
        if Sentence.objects.filter(sentence=self.sentence, section=section):
            raise AlreadyExistError()
        sentence = Sentence.objects.create(sentence=self.sentence, section=section)
        return sentence


class SentenceUpdateSchema(ModelSchema):
    new_sentence: str = Field(..., min_length=1)

    class Config:
        model = Sentence
        model_fields = ["id"]

    def to_model(self) -> Sentence:
        sentence = get_object_or_404(Sentence, pk=self.id)
        sentence.sentence = self.new_sentence
        sentence.save()
        return sentence


# Translations


class TranslationListSchema(ModelSchema):
    translator: OwnerSchema
    is_approved: bool
    score: int

    class Config:
        model = Translation
        model_fields = ["id", "translation", "translator", "created_at"]

    def resolve_is_approved(self, obj: Translation) -> bool:
        return obj.is_approved

    def resolve_score(self, obj: Translation) -> int:
        return obj.voters.all().count()


class TranslationSchema(ModelSchema):
    translator: OwnerSchema
    voters: list[OwnerSchema]
    sentence: SentenceSchema
    is_approved: bool
    score: int

    class Config:
        model = Translation
        model_fields = ["id", "translator", "sentence", "translation", "voters", "created_at"]

    def resolve_is_approved(self, obj: Translation) -> bool:
        return obj.is_approved

    def resolve_score(self, obj: Translation) -> int:
        return len(self.voters)


class TranslationCreateSchema(ModelSchema):
    class Config:
        model = Translation
        model_fields = ["sentence", "translation"]

    def to_model(self, translator) -> tuple[Translation, bool]:
        """Convert Schema to model. if similar translation found, add translator to voters else, create a new translation

        Args:
            translator (User): The user who want to translate the sentence.

        Returns:
            tuple[Translation, bool]: The old similar translation if found, else the new translation. For bool: True if this is a new translation else False.
        """
        sentence = get_object_or_404(Sentence, pk=self.sentence)
        tr = normalize_translation(self.translation)
        old_translations = sentence.translation_set.all()
        for trans in old_translations:
            trans.voters.remove(translator)
        match = get_close_match(
            tr, list(old_translations.values_list("translation", flat=True))
        )
        is_new = True
        if match:
            translation = Translation.objects.get(translation=match, sentence=sentence)
            translation.voters.add(translator)
            is_new = False
        else:
            translation = Translation.objects.create(
                translator=translator, sentence=sentence, translation=self.translation
            )
        return translation, is_new
