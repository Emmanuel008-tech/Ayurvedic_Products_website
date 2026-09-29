from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff/', include('backend.dashboard.urls')),
    path('staff', RedirectView.as_view(url='/staff/', permanent=True)),
    path('dashboard/', RedirectView.as_view(url='/staff/', permanent=True)),
    path('dashboard', RedirectView.as_view(url='/staff/', permanent=True)),
    path('', include('backend.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
