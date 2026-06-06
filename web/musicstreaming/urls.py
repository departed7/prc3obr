from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Автоматический редирект с пустой страницы на список треков
    path('', lambda request: redirect('music:track_list')),
    
    # Маршруты приложения музыки (включая вход/регистрацию)
    path('tracks/', include('music.urls')),
    
    # Маршруты приложения афиши (корзины билетов)
    path('billboard/', include('basket.urls')),
]

# Подключение статики и медиа (картинки, MP3, MP4)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)