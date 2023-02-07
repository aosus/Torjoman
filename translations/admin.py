from django.contrib import admin
from .models import Project, Section, Sentence, Translation

# Register your models here.
admin.site.register([Project, Section, Sentence, Translation])
