from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),
    # Serve default profile image cleanly at root (or redirect)
    path('default-profile.svg', RedirectView.as_view(url=settings.STATIC_URL + 'default-profile.svg')),
]

# Serve media files in development/local (even with Docker)
if settings.DEBUG or not settings.GS_BUCKET_NAME:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )

# Catch-all for Vue SPA (Must be LAST)
urlpatterns += [
    re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
]
