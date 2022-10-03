import hmac
import json
import threading
from hashlib import sha1

from django.conf import settings
from django.http import (HttpResponse, HttpResponseForbidden,
                         HttpResponseServerError)
from django.utils.encoding import force_bytes
from ninja import Router

from .tasks import handle_pr_comments, handle_push, handle_pull_request

router = Router()


@router.post("/")
def manage_webhooks(request):
    # Verify the request signature
    header_signature = request.META.get("HTTP_X_HUB_SIGNATURE")
    if header_signature is None:
        return HttpResponseForbidden("Permission denied.")

    sha_name, signature = header_signature.split("=")
    if sha_name != "sha1":
        return HttpResponseServerError("Operation not supported.", status=501)

    mac = hmac.new(
        force_bytes(settings.GITHUB_WEBHOOK_KEY),
        msg=force_bytes(request.body),
        digestmod=sha1,
    )
    if not hmac.compare_digest(force_bytes(mac.hexdigest()), force_bytes(signature)):
        return HttpResponseForbidden("Permission denied.")
    event = request.META.get("HTTP_X_GITHUB_EVENT", "ping")
    match event:
        case 'ping':
            return HttpResponse("pong")
        case "push":
            t = threading.Thread(target=handle_push, args=(json.loads(request.body),))
            t.start()
            return HttpResponse("success")
        case "pull_request":
            t = threading.Thread(target=handle_pull_request, args=(json.loads(request.body),))
            t.start()
            return HttpResponse("success")
        case "issue_comment":
            t = threading.Thread(target=handle_pr_comments, args=(json.loads(request.body),))
            t.start()
            return HttpResponse("success")
    return HttpResponse(status=204)
