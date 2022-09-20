from django.conf import settings
from ninja import NinjaAPI
from translation.api import router as translate_router
from translators.api import router as translators_router
from github_manager.webhook import router as github_manager_router


api = NinjaAPI(
	title='Torjoman Core API',
	version='1.0',
	description='This is the Torjoman Core API',
)

api.add_router("/translate", translate_router)
api.add_router("/accounts", translators_router)
api.add_router("/webhook", github_manager_router)
