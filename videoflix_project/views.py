from django.http import HttpResponseForbidden, FileResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
import os

# View to serve protected media files only to authenticated users
@login_required
def protected_media(request, path):
    # Construct the full file path based on the provided path
    media_path = os.path.join(settings.MEDIA_ROOT, path)

    # Check if the file exists
    if os.path.exists(media_path):
        # Serve the file as a response if it exists
        return FileResponse(open(media_path, "rb"))
    else:
        # If the file doesn't exist, return a forbidden error response
        return HttpResponseForbidden("Access denied or file not found.")
