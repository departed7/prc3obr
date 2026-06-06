from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api_views
from . import views

app_name = 'music'

router = DefaultRouter()
router.register(r'api-tracks', api_views.TrackViewSet)
router.register(r'api-playlists', api_views.PlaylistViewSet)
router.register(r'api-concerts', api_views.ConcertViewSet)

urlpatterns = [
    # API
    path('api/', include(router.urls)),

    # ТРЕКИ
    path('', views.TrackListView.as_view(), name='track_list'),
    path('track/<int:pk>/', views.TrackDetailView.as_view(), name='track_detail'),
    path('track/create/', views.TrackCreateView.as_view(), name='track_create'),
    path('track/<int:pk>/update/', views.TrackUpdateView.as_view(), name='track_update'),
    path('track/<int:pk>/delete/', views.TrackDeleteView.as_view(), name='track_delete'),
    
    # ФУНКЦИИ ПЛЕЕРА
    path('track/<int:pk>/like/', views.like_track, name='like_track'),
    path('track/<int:pk>/dislike/', views.dislike_track, name='dislike_track'),
    path('wave/', views.my_wave, name='my_wave'),

    # ПЛЕЙЛИСТЫ
    path('playlists/', views.PlaylistListView.as_view(), name='playlist_list'),
    path('playlist/<int:pk>/', views.PlaylistDetailView.as_view(), name='playlist_detail'),
    path('playlist/create/', views.PlaylistCreateView.as_view(), name='playlist_create'),
    path('playlist/<int:pk>/delete/', views.PlaylistDeleteView.as_view(), name='playlist_delete'),

    # КОЛЛЕКЦИИ
    path('collections/', views.CollectionListView.as_view(), name='collection_list'),
    path('collection/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),

    # АККАУНТ
    path('login/', views.login_user, name='login_page'),
    path('registration/', views.register_user, name='registration_page'),
    path('logout/', views.logout_user, name='logout_page'),
]