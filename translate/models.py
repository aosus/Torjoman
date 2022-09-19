from django.db import models


class Word(models.Model):
  word = models.CharField(max_length=255, unique=True)
  is_checked = models.BooleanField(default=False)
  class Meta:
    ordering = ['word']
  
  def get_source_translates(self) -> list[str]:
    return [translate.translate for translate in self.translate_set.all().order_by('score')]
  
  def get_users_translates(self) -> list[str]:
    return [translate.translate for translate in self.translate_set.all().order_by('score')]
    
  def __str__(self) -> str:
    return self.word

class TranslateBase(models.Model):
  word = models.ForeignKey(Word, on_delete=models.CASCADE)
  translate = models.CharField(max_length=255)
  
  class Meta:
    abstract = True
    
  def __str__(self) -> str:
    return f'{self.word}-{self.translate}'

class SourceTranslate(TranslateBase):
  is_default = models.BooleanField(default=False)
  
  def save(self, *args, **kwargs) -> None:
    if self.is_default:
      try:
        last_default_translate = SourceTranslate.objects.get(word=self.word, is_default=True)
        last_default_translate.is_default = False
        last_default_translate.save()
      except SourceTranslate.DoesNotExist:
        pass
    return super().save(*args, **kwargs)
  class Meta(TranslateBase.Meta):
    ordering = ('is_default',)

class UserTranslate(TranslateBase):
  score = models.PositiveIntegerField(default=0)   
  class Meta(TranslateBase.Meta):
    ordering = ('score',)
    

