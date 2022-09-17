from django.contrib import admin
from django.urls import path
from .api import api
# from github_manager.webhook import manage_webhooks

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
    # path('api/webhook/', manage_webhooks),
]
