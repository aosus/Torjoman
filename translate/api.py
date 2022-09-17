from difflib import SequenceMatcher
from typing import List
from django.shortcuts import get_object_or_404
from ninja import Router
from . import schemas
from django.conf import settings
from .models import Translate, Word
from source.models import Word as SourceWord
from translators.models import Translator
from ninja.errors import AuthenticationError
#This is for Arabic Only
import pyarabic.araby as araby


def do_before_check(word: str) -> str:
  return araby.strip_harakat(araby.strip_tatweel(word))

router = Router()

# @router.get("/", response={200: schemas.Word, 404: schemas.Error})
# def get_nontranslate_words(request):
#   words = SourceWord.objects.filter(translate=None).order_by('word')
#   if words.count() > 0:
#     return 200, words.first() # Get a random nontranslate word
  
#   words = SourceWord.objects.filter(is_checked=False).order_by('word')
#   if words.count() > 0:
#     return 200, words.first() # Get a random word not checked word
#   else:
#     return 404, {'messgae': 'there_are_no_nontranslate_words'}

@router.post("/", response=schemas.Word)
def recive_word(request, payload: schemas.WordIn):
  w: Word = get_object_or_404(Word, word=payload.word)
  try:
    translator: Translator = Translator.objects.get(uuid=payload.uuid)
    w.translators.add(translator)
    w.save()
  except Translator.DoesNotExist:
    raise AuthenticationError
  user_translate = do_before_check(payload.translate.strip())
  if user_translate == '': return w
  is_exists = (False, None)
  for t in w.translate_set.all():
    similarity = SequenceMatcher(None, t.translate, user_translate)
    print(similarity.ratio())
    print(similarity.quick_ratio())
    if similarity.ratio() > 0.8:
      is_exists = (True, t)
      break
  if not is_exists[0]:
    t = Translate(word=w, translate=user_translate)
    t.save()
  else:
    t: Translate = is_exists[1]
    t.score += 1
    t.save()
    
  return w