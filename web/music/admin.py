from django.contrib import admin
from .models import Category, Collection, Track, Playlist

admin.site.register(Category)
admin.site.register(Collection)
admin.site.register(Track)
admin.site.register(Playlist)