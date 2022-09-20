import uuid
from django.db import models

# Create your models here.
class Translator(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    number_of_words = models.IntegerField("Number of words to send")
    send_time = models.TimeField()
    translated_words = models.ManyToManyField("translation.Word", blank=True)

    def get_platforms(self):
        return [platform.name for platform in self.platform_set.all()]
    
    def __str__(self) -> str:
        return self.name

class Platform(models.Model):
  name = models.CharField(max_length=250)
  base_url = models.URLField()
  translators = models.ManyToManyField(Translator, blank=True)
  is_active = models.BooleanField(default=True) # if True, torjoman will send untranslated words to this platform

  @classmethod
  def get_all_platforms(cls) -> dict[str, "Platform"]:
    """get_all_platforms get a dict of all platforms.

    Returns:
      dict[str, Platform]: keys are platforms names, values are platforms instances
    """        
    return {
      f'{platform.name}': platform
      for platform in Platform.objects.all()
    }
  
  def __str__(self) -> str:
    return self.name