import random
from locust import HttpUser, TaskSet, SequentialTaskSet, task, between
from faker import Faker

fake = Faker('ru_RU')

class CatalogBrowsingTaskSet(TaskSet):

    @task(5)
    def view_track_catalog(self):
        self.client.get("/tracks/", name="GET /tracks/ (Каталог треков)")

    @task(5)
    def search_tracks(self):
        artists = ["MACAN", "The Weeknd", "Asti", "Bushido"]
        query = random.choice(artists)
        self.client.get(f"/tracks/?q={query}", name="GET /tracks/?q= (Поиск по артисту)")

    @task(5)
    def get_api_concerts(self):
        self.client.get("/tracks/api/api-concerts/", name="GET /api/api-concerts/ (JSON афиша)")

class AdminContentScenario(SequentialTaskSet):

    @task(5)
    def open_api_tracks_list(self):
        self.client.get("/tracks/api/api-tracks/", name="GET /api/api-tracks/ (JSON треки)")

    @task(1)
    def create_fake_track_post(self):
        fake_payload = {
            "title": fake.catch_phrase(),
            "artist": fake.name(),
            "lyrics": fake.text(max_nb_chars=100),
            "is_published": True
        }
        headers = {"Content-Type": "application/json"}
        with self.client.post("/tracks/api/api-tracks/", json=fake_payload, headers=headers, name="POST /api/api-tracks/ (Добавление трека)", catch_response=True) as resp:
            if resp.status_code in [200, 201, 403]:
                resp.success()
            else:
                resp.failure(f"Error {resp.status_code}")

class PulseLoadTestUser(HttpUser):
    wait_time = between(1, 2)
    tasks = {
        CatalogBrowsingTaskSet: 4,
        AdminContentScenario: 1
    }