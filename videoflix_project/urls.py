"""
URL configuration for videoflix_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from debug_toolbar.toolbar import debug_toolbar_urls
from videoflix_app.views import serve_protected_media 
from django.contrib.auth.decorators import login_required


urlpatterns =  [
        path("admin/", admin.site.urls),
        path("api/users/", include("users.urls")),
        path("api/", include("videoflix_app.urls")),
        path("django-rq/", include("django_rq.urls")),
    ]

# Debug-Modus: Medien direkt servieren
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Demo-Medien bleiben öffentlich
urlpatterns += static(settings.DEMO_MEDIA_URL, document_root=settings.DEMO_MEDIA_ROOT)

# Geschützte Medien für nicht-DEBUG-Modus
if not settings.DEBUG:
    urlpatterns += [
        path("protected_media/<path:path>", login_required(serve_protected_media), name="protected_media"),
    ]

# Debug Toolbar
urlpatterns += debug_toolbar_urls()


    # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # + static(settings.DEMO_MEDIA_URL, document_root=settings.DEMO_MEDIA_ROOT)
    # + debug_toolbar_urls()

