from django.contrib import admin

from .models import Moderator, PullRequest

# Register your models here.
admin.site.register(PullRequest)
admin.site.register(Moderator)
