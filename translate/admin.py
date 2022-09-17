from django.contrib import admin
from .models import Word, Translate
# Register your models here.
class TranslateAdminInline(admin.TabularInline):
  model = Translate

class WordAdmin(admin.ModelAdmin):
  inlines = (TranslateAdminInline, )
admin.site.register(Word, WordAdmin)
