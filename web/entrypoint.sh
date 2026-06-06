#!/bin/sh
set -e

echo "--- PULSE STARTUP ---"

# 1. Ждем базу данных
python <<'PY'
import os, socket, time
host = os.environ.get('DB_HOST_PGSQL', 'db')
port = int(os.environ.get('DB_PORT_PGSQL', '5432'))
while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print("Database is READY")
            break
    except OSError:
        time.sleep(1)
PY

# 2. Устанавливаем PYTHONPATH (это решит проблему с импортами)
export PYTHONPATH=$PYTHONPATH:/app

# 3. Выполняем команды Django (запускаем из корня /app)
echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static..."
python manage.py collectstatic --noinput

# 4. Запуск через Gunicorn
# Мы явно указываем путь к настройкам
echo "Starting Gunicorn..."
exec gunicorn --env DJANGO_SETTINGS_MODULE=musicstreaming.settings musicstreaming.wsgi:application --bind 0.0.0.0:8000 --workers 4