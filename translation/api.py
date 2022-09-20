from django.http import Http404
from django.shortcuts import get_object_or_404
from ninja import Router
from ninja.errors import AuthenticationError
from translators.models import Translator

from . import schemas
from .models import Word
from .utils import modify_translation

router = Router()


@router.post(
    "/",
    response={
        200: Word,
        404: Http404,
    },
)
def receiving_translation(request, payload: schemas.WordIn):
    w: Word = get_object_or_404(Word, word=payload.word)
    try:
        translator: Translator = Translator.objects.get(uuid=payload.uuid)
        w.translators.add(translator)
        w.save()
    except Translator.DoesNotExist:
        raise AuthenticationError
    tranlation = modify_translation(payload.translation)
    w.add_translation(tranlation)
    return {"success": True}
