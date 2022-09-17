from django.db import models

class Word(models.Model):
  word = models.CharField(max_length=255, unique=True)
  translators = models.ManyToManyField("translators.Translator")
    
  def get_translates(self) -> list["Translate"]:
    return [translate.translate for translate in self.translate_set.all().order_by('score')]
    
  def __str__(self) -> str:
    return self.word

class Translate(models.Model):
  word = models.ForeignKey(Word, on_delete=models.CASCADE)
  translate = models.CharField(max_length=255)
  score = models.IntegerField(default=1)

  def __str__(self) -> str:
    return f'{self.word}-{self.translate}'
