import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestKinopoiskUI:

    def test_homepage_loads_and_has_logo(self, browser):
        """Главная страница загружается и содержит логотип."""
        time.sleep(random.uniform(3, 5))
        assert "Кинопоиск" in browser.title, f"Title: {browser.title}"
        try:
            logo = browser.find_element(By.CSS_SELECTOR, "a[href='/']")
            assert logo.is_displayed()
        except:
            logo = browser.find_element(By.XPATH, "//*[contains(@alt, 'Кинопоиск') or contains(@class, 'logo')]")
            assert logo.is_displayed()

    def test_search_returns_relevant_results(self, browser):
        """Поиск фильма 'Матрица'."""
        time.sleep(random.uniform(3, 5))
        try:
            search_input = browser.find_element(By.NAME, "kp_query")
        except:
            search_input = browser.find_element(By.XPATH, "//input[@placeholder='Фильмы, сериалы, персоны']")

        search_input.clear()
        search_input.send_keys("Матрица")
        search_input.submit()
        time.sleep(random.uniform(5, 8))

        try:
            film_card = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'styles_root') or contains(@data-test-id, 'film')]"))
            )
            film_title = film_card.find_element(By.XPATH, ".//a[contains(@href, '/film/')]").text
        except:
            film_title = browser.find_element(By.XPATH, "//*[contains(text(), 'Матрица')][1]").text

        assert "Матрица" in film_title, f"Текст: {film_title}"

    def test_movie_page_displays_rating_and_year(self, browser):
        """Страница фильма — рейтинг и год (переходим по прямому URL)."""
        browser.get("https://www.kinopoisk.ru/film/301/")  # Матрица
        time.sleep(random.uniform(6, 10))

        browser.execute_script("window.scrollTo(0, 500);")
        time.sleep(3)

        # Рейтинг
        rating = None
        rating_selectors = [
            "//span[@data-tid='f4c5b4d4']",
            "//div[contains(@class, 'film-rating')]//span[1]",
            "//span[contains(@class, 'rating__value')]",
            "//span[contains(text(), '.') and string-length(text()) <= 4]"
        ]
        for selector in rating_selectors:
            try:
                element = WebDriverWait(browser, 15).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                text = element.text.strip()
                if any(char.isdigit() for char in text) and len(text) <= 5:
                    rating = text
                    break
            except:
                continue

        assert rating is not None, "Рейтинг не найден ни одним из селекторов"
        assert any(char.isdigit() for char in rating), f"Рейтинг: {rating}"

        # Год
        year = None
        year_selectors = [
            "//a[contains(@href, 'year=')]",
            "//span[contains(text(), '19') or contains(text(), '20')]",
            "//div[contains(text(), '19') or contains(text(), '20')]",
            "//time",
            "//*[contains(text(), '19') or contains(text(), '20')]"
        ]
        for selector in year_selectors:
            try:
                elements = browser.find_elements(By.XPATH, selector)
                for element in elements:
                    text = element.text
                    year_text = ''.join(filter(str.isdigit, text))
                    if len(year_text) == 4 and 1900 <= int(year_text) <= 2030:
                        year = year_text
                        break
                if year:
                    break
            except:
                continue

        assert year is not None, "Год не найден ни одним из селекторов"
        assert len(year) == 4 and 1900 <= int(year) <= 2030, f"Год: {year}"

    def test_navigation_to_person_page(self, browser):
        """Переход на страницу актёра (переходим по прямому URL фильма)."""
        browser.get("https://www.kinopoisk.ru/film/301/")  # Матрица
        time.sleep(random.uniform(6, 10))

        browser.execute_script("window.scrollTo(0, 1500);")
        time.sleep(3)

        actor = None
        actor_selectors = [
            "//a[contains(@href, '/name/') and not(contains(@href, '/film/'))][1]",
            "//div[contains(@data-test-id, 'actor')]//a[1]",
            "//span[contains(@class, 'actor-name')]//ancestor::a[1]"
        ]
        for selector in actor_selectors:
            try:
                actor = WebDriverWait(browser, 20).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                actor_name = actor.text.strip()
                if actor_name and len(actor_name) > 2:
                    break
            except:
                continue

        assert actor is not None, "Актёр не найден ни одним из селекторов"
        actor_name = actor.text.strip()
        assert actor_name, "Имя актёра пустое"
        browser.execute_script("arguments[0].scrollIntoView({block: 'center'});", actor)
        time.sleep(2)
        browser.execute_script("arguments[0].click();", actor)
        time.sleep(random.uniform(6, 10))
        assert actor_name in browser.title or actor_name in browser.page_source, f"Имя '{actor_name}' не найдено на странице"

    def test_search_input_exists_on_homepage(self, browser):
        """
        Проверка, что на главной странице присутствует поле поиска с атрибутом name="kp_query".
        """
        # Убедимся, что мы на главной
        if "kinopoisk.ru" not in browser.current_url:
            browser.get("https://www.kinopoisk.ru/")
            time.sleep(3)

        # Ищем поле поиска по атрибуту name — самый надёжный способ
        search_input = None
        selectors = [
            "//input[@name='kp_query']",
            "//input[@placeholder='Фильмы, сериалы, персоны']",
            "//input[contains(@class, 'search')]",
            "//form//input[@type='text']"
        ]

        for selector in selectors:
            try:
                search_input = WebDriverWait(browser, 15).until(
                    EC.presence_of_element_located((By.XPATH, selector))
                )
                if search_input:
                    print(f"✅ Поле поиска найдено по селектору: {selector}")
                    break
            except Exception as e:
                print(f"❌ Селектор не сработал: {selector} | Ошибка: {str(e)[:50]}...")
                continue

        # Главная проверка — наличие поля с атрибутом name="kp_query"
        assert search_input is not None, "❌ Поле поиска не найдено ни одним из селекторов"
        assert search_input.get_attribute("name") == "kp_query", f"❌ Атрибут name не равен 'kp_query', а равен '{search_input.get_attribute('name')}'"

        # Дополнительно: проверяем, что поле видимо и активно
        assert search_input.is_displayed(), "❌ Поле поиска не отображается"
        assert search_input.is_enabled(), "❌ Поле поиска не активно"

        print("✅ Поле поиска успешно найдено и проверено!")