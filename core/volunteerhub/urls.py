# File: volunteerhub/urls.py
# Purpose:
#   Central routing for the entire VolunteerHub project.
#   HTML page routes come from signups.views.
#   API endpoints come from signups.api_urls.

from django.contrib import admin
from django.urls import path, include
from signups import views as signups_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Main visual landing page with volunteer background
    path("", signups_views.landing_page, name="main-landing"),

    # Unified signup/signin flow
    path("auth/", signups_views.unified_auth_page, name="unified-auth"),

    # Include all signups URLs (this handles all the page routes)
    path("", include("signups.urls")),

    # API namespace
    path("api/", include("signups.api_urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
