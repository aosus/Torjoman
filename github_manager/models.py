from django.db import models


# Create your models here.
class PullRequest(models.Model):
    number = models.IntegerField()
    word = models.ForeignKey("translation.Word", on_delete=models.CASCADE)


class Moderator(models.Model):
    username = models.CharField(max_length=255)

    @classmethod
    def get_all_moderators(cls) -> list[str]:
        return [mod.username for mod in cls.objects.all()]
