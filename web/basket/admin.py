from django.contrib import admin
from .models import Concert

@admin.register(Concert)
class ConcertAdmin(admin.ModelAdmin):
    list_display = ('artist', 'city', 'date', 'price')
    list_filter = ('city', 'date')
    search_fields = ('artist', 'title')