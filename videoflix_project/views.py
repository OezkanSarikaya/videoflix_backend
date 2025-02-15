from django.http import HttpResponseForbidden, FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os

@login_required
def protected_media(request, path):
    media_path = os.path.join(settings.MEDIA_ROOT, path)
    
    if os.path.exists(media_path):
        return FileResponse(open(media_path, 'rb'))
    else:
        return HttpResponseForbidden("Zugriff verweigert oder Datei nicht gefunden.")