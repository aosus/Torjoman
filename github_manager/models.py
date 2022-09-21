from django.db import models


# Create your models here.
class PullRequest(models.Model):
    prid = models.IntegerField()
    words = models.ManyToManyField("translation.Word", blank=True)
