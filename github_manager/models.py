from django.db import models


# Create your models here.
class PullRequest(models.Model):
    number = models.IntegerField()
    word = models.ForeignKey("translation.Word", on_delete=models.CASCADE)

class Moderator(models.Model):
    username = models.CharField(max_length=255)
    
    @property
    def get_all_moderators(self) -> list[str]:
        """get_all_moderators Return a list of moderators usernames

        Returns:
            list[str]: The list of moderators usernames
        """        
        return [mod.username for mod in Moderator.objects.all()]