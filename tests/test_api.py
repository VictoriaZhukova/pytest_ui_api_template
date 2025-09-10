import os
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
        """Поиск по кириллице → 200 OK"""
        query = "Сумерки"
        response = requests.get(f"{BASE_URL}/movie/search", headers=HEADERS, params={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert len(data["docs"]) > 0
        assert any(query in (doc.get("name", "") + doc.get("alternativeName", "")) for doc in data["docs"])

    def test_search_movie_latin_success(self):
        """Поиск по латинице → 200 OK"""
        query = "The Matrix"
        response = requests.get(f"{BASE_URL}/movie/search", headers=HEADERS, params={"query": query})
        assert response.status_code == 200
        data = response.json()
        assert len(data["docs"]) > 0
        assert any(query.lower() in (doc.get("name", "") + doc.get("alternativeName", "")).lower() for doc in data["docs"])

    def test_search_movie_by_id_success(self):
        """Получение по ID → 200 OK"""
        movie_id = 301  # Матрица
        response = requests.get(f"{BASE_URL}/movie/{movie_id}", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == movie_id

    def test_search_movie_with_emoji_returns_200_but_empty(self):
        """Смайлик → 200, но пустой результат"""
        emoji = "%F0%9F%98%81"
        response = requests.get(f"{BASE_URL}/movie/search?query={emoji}", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert len(data.get("docs", [])) == 0

    def test_search_movie_with_1000_symbols_returns_200_but_empty(self):
        """1000 символов → 200, но пустой результат"""
        long_str = "A" * 1000
        response = requests.get(f"{BASE_URL}/movie/search", headers=HEADERS, params={"query": long_str})
        assert response.status_code == 200
        data = response.json()
        assert len(data.get("docs", [])) == 0

    def test_search_movie_with_double_space_returns_200_but_not_relevant(self):
        """Два пробела → 200, но результаты не релевантны (не содержат пустых названий)"""
        response = requests.get(f"{BASE_URL}/movie/search?query=%20%20", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        # Проверяем, что ни один фильм не имеет пустого названия
        assert all(doc.get("name", "").strip() != "" for doc in data.get("docs", []))

    def test_search_movie_with_nonsense_cyrillic_returns_200_but_empty(self):
        """Бессмысленный набор букв → 200, но пустой результат"""
        nonsense = "%D0%B2%D0%B0%D0%B0%D1%80%D0%BA%D0%B3%D1%8B%D0%BF%D1%84%D0%BC%D0%B0%D1%8B"
        response = requests.get(f"{BASE_URL}/movie/search?query={nonsense}", headers=HEADERS)
        assert response.status_code == 200
        data = response.json()
        assert len(data.get("docs", [])) == 0

    def test_search_movie_with_invalid_id_returns_400(self):
        """Несуществующий ID → 400 Bad Request (раньше было 404)"""
        invalid_id = 999999999
        response = requests.get(f"{BASE_URL}/movie/{invalid_id}", headers=HEADERS)
        assert response.status_code == 400  # Было 404, стало 400