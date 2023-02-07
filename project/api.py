from ninja_extra import NinjaExtraAPI
from accounts.api import AccountsController
from accounts.utils import AuthBearer
from translations.api import ProjectController, SectionController, SentenceController, TranslationController

api = NinjaExtraAPI(
    title="Torjoman's Core API",
    version="0.1.0",
    description="This is the Torjoman's core API",
    auth=AuthBearer()
)

api.register_controllers(
    ProjectController,
    SectionController,
    SentenceController,
    TranslationController,
    AccountsController,
)