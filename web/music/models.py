from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
import os
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.oggvorbis import OggVorbis

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Жанр')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    def __str__(self): return self.name
    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

class Collection(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название подборки')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    def __str__(self): return self.name
    class Meta:
        verbose_name = 'Подборка'
        verbose_name_plural = 'Подборки'

class Track(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название трека')
    artist = models.CharField(max_length=255, verbose_name='Исполнитель')
    duration = models.PositiveIntegerField(default=0, verbose_name='Длительность', editable=False)
    
    cover = models.ImageField(
        upload_to='covers/%Y/%m/%d/', 
        blank=True, null=True, 
        verbose_name='Обложка',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])]
    )
    
    vibe_video = models.FileField(
        upload_to='vibes/%Y/%m/%d/', 
        blank=True, null=True, 
        verbose_name='Vibe-видео (MP4)', 
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    
    # Сделал null=True для работы скрипта заполнения, потом загрузишь файлы сам
    audio_file = models.FileField(
        upload_to='tracks/%Y/%m/%d/', 
        verbose_name='Аудиофайл',
        null=True, blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['mp3', 'wav', 'ogg'])]
    )
    
    lyrics = models.TextField(blank=True, null=True, verbose_name='Текст песни')
    
    likes = models.ManyToManyField(User, related_name='liked_tracks', blank=True, verbose_name='Понравилось')
    dislikes = models.ManyToManyField(User, related_name='disliked_tracks', blank=True, verbose_name='Не нравится')
    
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    play_count = models.PositiveIntegerField(default=0, verbose_name='Количество прослушиваний')
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name='Категория', null=True, blank=True)
    collections = models.ManyToManyField(Collection, blank=True, verbose_name='Коллекции')

    def save(self, *args, **kwargs):
        if self.audio_file:
            super().save(*args, **kwargs)
            try:
                file_path = self.audio_file.path
                ext = os.path.splitext(file_path)[1].lower()
                if ext == '.mp3': audio = MP3(file_path)
                elif ext == '.wav': audio = WAVE(file_path)
                elif ext == '.ogg': audio = OggVorbis(file_path)
                self.duration = int(audio.info.length)
            except:
                self.duration = 0
        super().save(*args, **kwargs)

    def __str__(self): return f'{self.artist} - {self.title}'

    class Meta:
        verbose_name = 'Трек'
        verbose_name_plural = 'Треки'

class Playlist(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название плейлиста')
    cover = models.ImageField(upload_to='playlists/%Y/%m/%d/', blank=True, null=True, verbose_name='Обложка')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    tracks = models.ManyToManyField(Track, blank=True, verbose_name='Треки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    # Адаптация склонения слова "трек" (1 трек, 2 трека, 5 треков)
    def get_track_count_text(self):
        count = self.tracks.count()
        if count % 10 == 1 and count % 100 != 11:
            return f"{count} трек"
        elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
            return f"{count} трека"
        else:
            return f"{count} треков"

    def __str__(self): return self.name

    class Meta:
        verbose_name = 'Плейлист'
        verbose_name_plural = 'Плейлисты'