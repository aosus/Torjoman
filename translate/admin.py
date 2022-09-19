from django.contrib import admin
from .models import Word, UserTranslate
# Register your models here.
class TranslateAdminInline(admin.TabularInline):
  model = UserTranslate

class WordAdmin(admin.ModelAdmin):
  inlines = (TranslateAdminInline, )
admin.site.register(Word, WordAdmin)
