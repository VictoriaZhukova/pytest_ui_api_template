# pytest_ui_api_template


## Дипломная работа по автоматизации тестирования на python

### Шаги:
1. Склонировать проект 'https://github.com/VictoriaZhukova/pytest_ui_api_template.git'
2. Установить все зависимости
3. Запустить тесты 'pytest'

### Стек:
- pytest
- selenium
- requests
- allure
- config

### Струткура:
- ./test - UI- и API-тесты
- ./allure-results - результаты

### Полезные ссылки
- [Подсказка по markdown](https://www.markdownguide.org/basic-syntax/)
- [Генератор файла .gitignore](https://www.toptal.com/developers/gitignore)
- [Ссылка на проект](https://zhukova-victoria.yonote.ru/share/49f4215a-c537-4d8b-a789-e970aff7cac4)

### Библиотеки (!)
- pyp install pytest
- pip install selenium
- pip install webdriver-manager

### Как добавить API-ключ
1. Получить API-ключ
Перейти в Telegram и написать боту: @kinopoiskdev_bot
Отправить команду: /start

2. Бот выдаст уникальный API-ключ вида:
ABC123-XYZ456-789KLM-NOP012

3. Скопировать код и добавить в .env вместо "ключ_сюда".