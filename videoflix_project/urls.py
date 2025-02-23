from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from videoflix_app.views import serve_protected_media

# Define URL paths for the application
urlpatterns = [
    # Admin panel URL
    path("admin/", admin.site.urls),
    
    # User-related API URLs
    path("api/users/", include("users.urls")),
    
    # Main application API URLs
    path("api/", include("videoflix_app.urls")),
    
    # URL for Django RQ
    path("django-rq/", include("django_rq.urls")),
]

# Serve media files in DEBUG mode directly from the filesystem
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve demo media files publicly (accessible to anyone)
urlpatterns += static(settings.DEMO_MEDIA_URL, document_root=settings.DEMO_MEDIA_ROOT)

# Serve protected media files in production (only authenticated users can access)
if not settings.DEBUG:
    urlpatterns += [
        path("protected_media/<path:path>", serve_protected_media, name="protected_media"),
    ]

# Add debug toolbar URLs for development purposes
urlpatterns += debug_toolbar_urls()
