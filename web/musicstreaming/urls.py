from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

import django_prometheus.exports
from music.metrics import update_db_metrics

def metrics_view(request):
    update_db_metrics()
    return django_prometheus.exports.ExportToDjangoView(request)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('music:track_list')),
    path('tracks/', include('music.urls')),
    path('billboard/', include('basket.urls')),
    
    path('', include('django_prometheus.urls')),
    path('metrics', metrics_view, name='prometheus-metrics'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)