from ninja_extra import api_controller, ControllerBase, route
from .schemas import *
from .models import Project, Sentence
from django.shortcuts import get_list_or_404
from ninja_extra.pagination import (
    paginate,
    PageNumberPaginationExtra,
    PaginatedResponseSchema,
)
from .errors import *


@api_controller("projects/")
class ProjectController(ControllerBase):
    @route.get("", auth=None)
    @paginate(PageNumberPaginationExtra, page_size=25)
    def list_projects(
        self, username: str = None
    ) -> PaginatedResponseSchema[ProjectSchema]:
        if username:
            user = get_object_or_404(User, username=username)
            projects = Project.objects.filter(owner=user)
        else:
            projects = Project.objects.all()
        return projects

    @route.post("")
    def create_project(self, request, payload: ProjectCreateSchema) -> ProjectSchema:
        project = payload.to_model(request.auth)
        return project

    @route.post("update")
    def update_project(self, request, payload: ProjectUpdateSchema) -> ProjectSchema:
        project = get_object_or_404(Project, pk=payload.id)
        if project.owner != request.auth:
            raise PermissionError()
        project = payload.to_model(request.auth)
        return project


@api_controller("sections/")
class SectionController(ControllerBase):
    @route.get("", auth=None)
    def list_project_sections(self, project: int) -> list[SectionSchema]:
        sections = Section.objects.filter(project=project)
        return sections

    @route.post("")
    def create_section(self, request, payload: SectionCreateSchema) -> SectionSchema:
        project = get_object_or_404(Project, pk=payload.project)
        if project.owner != request.auth:
            raise PermissionError()
        section = payload.to_model()
        return section

    @route.post("update")
    def update_section(self, request, payload: SectionUpdateSchema) -> SectionSchema:
        section = get_object_or_404(Section, pk=payload.id)
        if section.project.owner != request.auth:
            raise PermissionError()
        section = payload.to_model()
        return section


@api_controller("sentence/")
class SentenceController(ControllerBase):
    @route.get("", auth=None)
    @paginate(PageNumberPaginationExtra, page_size=50)
    def list_section_sentences(
        self, section: int
    ) -> PaginatedResponseSchema[SentenceSchema]:
        sentences = Sentence.objects.filter(section=section)
        return sentences

    @route.post("")
    def create_sentence(self, request, payload: SentenceCreateSchema) -> SentenceSchema:
        section = get_object_or_404(Section, pk=payload.section)
        if section.project.owner != request.auth:
            raise PermissionError()
        sentence = payload.to_model()
        return sentence

    @route.post("update")
    def update_sentence(self, request, payload: SentenceUpdateSchema) -> SentenceSchema:
        sentence = get_object_or_404(Sentence, pk=payload.id)
        if sentence.section.project.owner != request.auth:
            raise PermissionError()
        sentence = payload.to_model()
        return sentence


@api_controller("translation/")
class TranslationController(ControllerBase):
    @route.get("", auth=None)
    @paginate(PageNumberPaginationExtra, page_size=20)
    def list_sentence_translation(
        self, sentence: int
    ) -> PaginatedResponseSchema[TranslationListSchema]:
        translations = Translation.objects.filter(sentence=sentence)
        return translations

    @route.get("{id}", auth=None)
    def get_translation(self, id: int) -> TranslationSchema:
        translation = get_object_or_404(Translation, pk=id)
        return translation

    @route.post("")
    def create_translation(
        self, request, payload: TranslationCreateSchema
    ) -> TranslationSchema:
        translations_of_translator = Translation.objects.filter(
            translator=request.auth, sentence=payload.sentence
        ).count()
        if translations_of_translator >= 5:
            raise LimitError()
        translation, _ = payload.to_model(translator=request.auth)
        return translation
