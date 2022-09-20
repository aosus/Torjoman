from django.contrib import admin
from .models import Word, UserTranslation, SourceTranslation

# Register your models here.


class UserTranslationAdminInline(admin.TabularInline):
    model = UserTranslation


class SourceTranslationAdminInline(admin.TabularInline):
    model = SourceTranslation


class WordAdmin(admin.ModelAdmin):
    inlines = (SourceTranslationAdminInline, UserTranslationAdminInline)


admin.site.register(Word, WordAdmin)
