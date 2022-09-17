import hmac
from hashlib import sha1
import json
from ninja import Router
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseServerError
from django.utils.encoding import force_bytes
from .tasks import push
import threading


router = Router()

@router.post('/')
def manage_webhooks(request):
  # Verify the request signature
  header_signature = request.META.get('HTTP_X_HUB_SIGNATURE')
  if header_signature is None:
    return HttpResponseForbidden('Permission denied.')

  sha_name, signature = header_signature.split('=')
  if sha_name != 'sha1':
    return HttpResponseServerError('Operation not supported.', status=501)

  mac = hmac.new(force_bytes(settings.GITHUB_WEBHOOK_KEY), msg=force_bytes(request.body), digestmod=sha1)
  if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
    return HttpResponseForbidden('Permission denied.')

  # If request reached this point we are in a good shape
  # Process the GitHub events
  event = request.META.get('HTTP_X_GITHUB_EVENT', 'ping')

  if event == 'ping':
    return HttpResponse('pong')
  elif event == 'push':
    t = threading.Thread(target=push, args=(json.loads(request.body),))
    t.start()
    return HttpResponse('success')
  # In case we receive an event that's not ping or push
  return HttpResponse(status=204)