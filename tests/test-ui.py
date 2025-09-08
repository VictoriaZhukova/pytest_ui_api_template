from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestKinopoiskUI:

    def test_homepage_loads_and_has_logo(self, browser):
        """Главная страница загружается и содержит логотип."""
        assert "Кинопоиск" in browser.title
        logo = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
        )
        assert logo.is_displayed()

    def test_search_returns_relevant_results(self, browser):
        """Поиск фильма 'Интерстеллар' возвращает релевантные результаты."""
        search_input = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.NAME, "kp_query"))
        )
        search_input.clear()
        search_input.send_keys("Интерстеллар")
        search_input.submit()

        first_result = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".styles_root__ti07r"))
        )
        assert "Интерстеллар" in first_result.text

    def test_movie_page_displays_rating_and_year(self, browser):
        """Страница фильма отображает рейтинг и год выпуска."""
        top_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Топ-250"))
        )
        top_link.click()

        first_film_link = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-id='film-list-item'] a"))
        )
        first_film_link.click()

        rating_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span[data-tid='f4c5b4d4']"))
        )
        year_element = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='/film/'] + a"))
        )

        rating_text = rating_element.text.strip()
        year_text = year_element.text.strip()

        assert rating_text and any(char.isdigit() for char in rating_text)
        assert year_text.isdigit() and len(year_text) == 4

    def test_navigation_to_person_page(self, browser):
        """Переход на страницу актёра работает корректно."""
        top_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Топ-250"))
        )
        top_link.click()

        first_film_link = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-test-id='film-list-item'] a"))
        )
        first_film_link.click()

        actor_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "div[data-test-id='actor-list-item'] a"))
        )
        actor_name = actor_link.text
        actor_link.click()

        WebDriverWait(browser, 10).until(EC.title_contains(actor_name))
        assert actor_name in browser.title

    def test_footer_links_are_clickable(self, browser):
        """Ссылки в футере кликабельны."""
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        footer_link = WebDriverWait(browser, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Пользовательское соглашение"))
        )
        original_url = browser.current_url
        footer_link.click()

        WebDriverWait(browser, 10).until(lambda d: d.current_url != original_url)
        assert "rules" in browser.current_url or "пользовательское соглашение" in browser.title.lower()