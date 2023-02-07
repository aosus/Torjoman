from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.template.defaultfilters import slugify

# Create your models here.


class Project(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["owner", "name"]

    def __str__(self):
        return self.name


class Section(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)
        unique_together = ["project", "name"]

    def __str__(self):
        return f"{self.project}[{self.name}]"


class Sentence(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    sentence = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("section", "sentence")
        unique_together = ["section", "sentence"]

    def save(self, *args, **kwargs):
        self.context = self.context.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.section}: {self.sentence[:10]}"


class Translation(models.Model):
    translator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    sentence = models.ForeignKey(Sentence, on_delete=models.CASCADE)
    translation = models.TextField()
    voters = models.ManyToManyField(User, blank=True, related_name="voters")
    approved_by = models.ForeignKey(
        User,
        blank=True,
        null=True,
        related_name="approved_by",
        on_delete=models.SET_NULL,
    )
    approved_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Do not modify this value, it will be added automatically",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def is_approved(self):
        return True if self.approved_at else False

    def save(self, *args, **kwargs):
        if self.approved_by and not self.approved_at:
            self.approved_at = now()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.sentence} - {self.translation[:30]}"
