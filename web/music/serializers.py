from rest_framework import serializers
from .models import Track, Playlist, Collection, Category
from basket.models import Concert

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TrackSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = Track
        exclude = ['likes', 'dislikes']

class PlaylistSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    track_count = serializers.IntegerField(source='tracks.count', read_only=True)

    class Meta:
        model = Playlist
        fields = ['id', 'name', 'user_name', 'track_count', 'cover', 'is_public']

class ConcertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concert
        fields = '__all__'