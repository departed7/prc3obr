from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.db.models import Q
from .models import Track, Playlist, Collection
import random

class FormStyleMixin:
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
            if field_name == 'cover': field.widget.attrs.update({'accept': 'image/*'})
            if field_name == 'audio_file': field.widget.attrs.update({'accept': 'audio/mpeg, audio/wav, audio/ogg'})
            if field_name == 'vibe_video': field.widget.attrs.update({'accept': 'video/mp4'})
        return form

# --- АВТОРИЗАЦИЯ ---
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('music:track_list')
    else: form = AuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('music:track_list')
    else: form = UserCreationForm()
    return render(request, 'auth/registration.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('music:track_list')

# --- ТРЕКИ ---
class TrackListView(ListView):
    model = Track
    template_name = 'tracks/track_list.html'
    context_object_name = 'tracks'
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Track.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))
        return Track.objects.all()

class TrackDetailView(DetailView):
    model = Track
    template_name = 'tracks/track_detail.html'
    context_object_name = 'track'

@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class TrackCreateView(FormStyleMixin, CreateView):
    model = Track
    fields = ['title', 'artist', 'cover', 'vibe_video', 'audio_file', 'lyrics', 'category', 'collections']
    template_name = 'tracks/track_form.html'
    success_url = reverse_lazy('music:track_list')

@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class TrackUpdateView(FormStyleMixin, UpdateView):
    model = Track
    fields = ['title', 'artist', 'cover', 'vibe_video', 'audio_file', 'lyrics', 'category', 'collections']
    template_name = 'tracks/track_form.html'
    success_url = reverse_lazy('music:track_list')

@method_decorator(user_passes_test(lambda u: u.is_staff), name='dispatch')
class TrackDeleteView(DeleteView):
    model = Track
    template_name = 'tracks/track_confirm_delete.html'
    success_url = reverse_lazy('music:track_list')

# --- ФУНКЦИИ ПЛЕЕРА ---
@login_required
def like_track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if request.user in track.likes.all(): track.likes.remove(request.user)
    else:
        track.likes.add(request.user)
        track.dislikes.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'music:track_list'))

@login_required
def dislike_track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if request.user in track.dislikes.all(): track.dislikes.remove(request.user)
    else:
        track.dislikes.add(request.user)
        track.likes.remove(request.user)
    return redirect('music:my_wave')

def my_wave(request):
    all_tracks = Track.objects.all()
    if request.user.is_authenticated:
        all_tracks = all_tracks.exclude(dislikes=request.user)
    if not all_tracks.exists(): return redirect('music:track_list')
    random_track = random.choice(all_tracks)
    return render(request, 'tracks/track_detail.html', {'track': random_track, 'is_wave': True})

# --- ПЛЕЙЛИСТЫ ---
class PlaylistListView(ListView):
    model = Playlist
    template_name = 'playlists/playlist_list.html'
    context_object_name = 'playlists'

class PlaylistDetailView(DetailView):
    model = Playlist
    template_name = 'playlists/playlist_detail.html'
    context_object_name = 'playlist'

class PlaylistCreateView(FormStyleMixin, CreateView):
    model = Playlist
    fields = ['name', 'cover', 'tracks']
    template_name = 'playlists/playlist_form.html'
    success_url = reverse_lazy('music:playlist_list')
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PlaylistDeleteView(DeleteView):
    model = Playlist
    template_name = 'playlists/playlist_confirm_delete.html'
    success_url = reverse_lazy('music:playlist_list')

# --- КОЛЛЕКЦИИ ---
class CollectionListView(ListView):
    model = Collection
    template_name = 'collections/collection_list.html'
    context_object_name = 'collections'

class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'collections/collection_detail.html'
    context_object_name = 'collection'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tracks'] = self.object.track_set.all()
        return context