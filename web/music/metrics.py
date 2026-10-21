from prometheus_client import Gauge
from music.models import Track
from django.contrib.auth.models import User

tracks_count_gauge = Gauge('pulse_tracks_total_count', 'Total number of music tracks in PULSE')
users_count_gauge = Gauge('pulse_registered_users_total', 'Total number of registered users in PULSE')

def update_db_metrics():
    try:
        tracks_count_gauge.set(Track.objects.count())
        users_count_gauge.set(User.objects.count())
    except Exception:
        pass