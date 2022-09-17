import uuid
from django.db import models

# Create your models here.
class Translator(models.Model):
  uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
  name = models.CharField(max_length=255)
  number_of_words = models.IntegerField('Number of words to send')
  send_time = models.TimeField()
  
  def __str__(self) -> str:
    return self.name
  
class Platform(models.Model):
  name = models.CharField(max_length=250)
  base_url = models.URLField()
  translators = models.ManyToManyField(Translator, blank=True)
  is_active = models.BooleanField(default=True)
  
  def __str__(self) -> str:
    return self.name