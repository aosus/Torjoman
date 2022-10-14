from django.contrib import admin

from .models import Platform, Translator

# Register your models here.
admin.site.register(Translator)
admin.site.register(Platform)
