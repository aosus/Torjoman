from ninja import Router
from . import schemas
from .models import Translator, Platform

router = Router()
  
  
@router.post("/register", response={200: schemas.Translator, 400: schemas.Error, 404: schemas.Error})
def register(request, payload: schemas.TranslatorRegister):
  platforms: dict[str, Platform] = {f'{platform.name}': platform for platform in Platform.objects.all()}
  platforms_names = list(platforms.keys())
  if payload.platform not in platforms_names:
    return 400, schemas.Error(message='platform_not_exists')
  translator = Translator(name=payload.name, number_of_words=payload.number_of_words, send_time=payload.send_time)
  translator.save()
  platform = platforms[payload.platform]
  platform.translators.add(translator)
  platform.save()
  return 200, translator


@router.post("/login", response={200: schemas.Translator, 400: schemas.Error, 404: schemas.Error})
def login(request, payload: schemas.TranslatorLogin):
  try: translator = Translator.objects.get(uuid=payload.uuid)
  except: return 404, schemas.Error(message='user_not_exists')
  platforms: dict[str, Platform] = {f'{platform.name}': platform for platform in Platform.objects.all()}
  platforms_names = list(platforms.keys())
  if payload.platform not in platforms_names:
    return 400, schemas.Error(message='platform_not_exists')
  platform = platforms[payload.platform]
  platform.translators.add(translator)
  platform.save()
  return 200, translator

