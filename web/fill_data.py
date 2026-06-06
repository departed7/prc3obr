import os
import django
import datetime
import random
from django.utils import timezone

# Установка окружения Django (название папки с настройками остается прежним)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'musicstreaming.settings')
django.setup()

# Импорт моделей напрямую
from music.models import Category, Collection, Track
from basket.models import Concert
from django.contrib.auth.models import User

def populate():
    print("--- ЗАПОЛНЕНИЕ PULSE ДАННЫМИ 2026 (DOCKER MODE) ---")
    
    # 1. Жанры
    genres = ['Hip-Hop', 'Pop', 'Chanson', 'Rock', 'Electronic']
    genre_objs = {}
    for g in genres:
        obj, _ = Category.objects.get_or_create(name=g)
        genre_objs[g] = obj

    # 2. Коллекции
    col_objs = []
    for c in ['Топ-100 Россия 2026', 'Моя волна', 'Легенды жанра']:
        obj, _ = Collection.objects.get_or_create(name=c)
        col_objs.append(obj)

    # 3. Афиша
    concerts = [
        {'artist': 'MACAN', 'title': 'I AM Tour', 'city': 'Москва', 'price': 3500, 'venue': 'Лужники'},
        {'artist': 'Bushido Zho', 'title': 'VODALAZ', 'city': 'СПб', 'price': 2500, 'venue': 'A2'},
        {'artist': 'Anna Asti', 'title': 'Царица', 'city': 'Сочи', 'price': 5000, 'venue': 'New Wave Hall'},
    ]
    for con in concerts:
        Concert.objects.get_or_create(
            artist=con['artist'], title=con['title'], city=con['city'],
            venue=con['venue'], price=con['price'],
            date=timezone.now() + datetime.timedelta(days=random.randint(10, 50))
        )

    # 4. ТРЕКИ
    tracks_data = [
        {'title': 'Blinding Lights 2', 'artist': 'The Weeknd', 'genre': 'Pop', 'lyrics': 'I said, ooh, I am blinded by the lights...'},
        {'title': 'За деньги да', 'artist': 'Instasamka', 'genre': 'Pop', 'lyrics': 'Эту сумку мне муж купил...'},
        {'title': 'Блондинка', 'artist': 'Bushido Zho', 'genre': 'Hip-Hop', 'lyrics': 'Да, она блондинка...'},
    ]
    for t in tracks_data:
        track, created = Track.objects.get_or_create(
            title=t['title'],
            artist=t['artist'],
            category=genre_objs[t['genre']],
            lyrics=t['lyrics']
        )
        if created:
            track.collections.add(random.choice(col_objs))

    print("[!] ГОТОВО. База PULSE наполнена.")

if __name__ == '__main__':
    populate()