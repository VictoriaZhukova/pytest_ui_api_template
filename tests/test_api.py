import os
import pytest
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("KINOPOISK_API_URL", "https://api.kinopoisk.dev/v1.4")
API_KEY = os.getenv("KINOPOISK_API_KEY")

HEADERS = {
    "X-API-KEY": API_KEY,
    "Content-Type": "application/json"
}

if not API_KEY:
    raise EnvironmentError("❌ Укажите KINOPOISK_API_KEY в файле .env")


class TestKinopoiskAPIChecklist:

    def test_search_movie_cyrillic_success(self):
        """
        [Позитивный №1] Поиск фильма по названию на кириллице → 200 OK
        Пример: query=Сумерки
        """
        query = "Сумерки"
        url = f"{BASE_URL}/movie/search"
        params = {"page": 1, "limit": 10, "query": query}

        response = requests.get(url, headers=HEADERS, params=params)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        json_data = response.json()

        assert "docs" in json_data, "Нет поля 'docs'"
        assert len(json_data["docs"]) > 0, "Нет результатов поиска"
        assert any(query in doc.get("name", "") for doc in json_data["docs"]), "Название не найдено в результатах"

    def test_search_movie_latin_success(self):
        """
        [Позитивный №2] Поиск фильма по названию на латинице → 200 OK
        Пример: query=Twilight
        """
        query = "Twilight"
        url = f"{BASE_URL}/movie/search"
        params = {"page": 1, "limit": 10, "query": query}

        response = requests.get(url, headers=HEADERS, params=params)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        json_data = response.json()

        assert "docs" in json_data, "Нет поля 'docs'"
        assert len(json_data["docs"]) > 0, "Нет результатов поиска"
        assert any(query.lower() in doc.get("name", "").lower() for doc in json_data["docs"]), "Название не найдено"

    def test_search_movie_by_id_success(self):
        """
        [Позитивный №3] Получение фильма по ID → 200 OK
        Пример: movie/401177
        """
        movie_id = 401177
        url = f"{BASE_URL}/movie/{movie_id}"

        response = requests.get(url, headers=HEADERS)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"
        json_data = response.json()

        assert json_data.get("id") == movie_id, "ID не совпадает"
        assert "name" in json_data and isinstance(json_data["name"], str), "Нет корректного названия"

    def test_search_movie_with_emoji_returns_400(self):
        """
        [Негативный №4] Поиск с эмодзи 😁 → 400 Bad Request
        query=%F0%9F%98%81
        """
        emoji_encoded = "%F0%9F%98%81"  # 😁
        url = f"{BASE_URL}/movie/search?page=1&limit=10&query={emoji_encoded}"

        response = requests.get(url, headers=HEADERS)

        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}"
        assert "message" in response.json(), "Нет сообщения об ошибке"

    def test_search_movie_with_1000_symbols_returns_404(self):
        """
        [Негативный №5] Поиск с 1000 символов → 404 Not Found
        """
        long_query = "A" * 1000
        url = f"{BASE_URL}/movie/search"
        params = {"page": 1, "limit": 10, "query": long_query}

        response = requests.get(url, headers=HEADERS, params=params)

        assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"
        assert "message" in response.json(), "Нет сообщения об ошибке"