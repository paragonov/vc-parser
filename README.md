# Scraper
Приложение позволяет получить информацию о видеокартах через Telegram бота, по заданным параметрам в фильтрации.

### Технологии:
- Python 3.10
- Django 4.1.1 / Django Rest Framework 3.13.1
- PostgreSQL 14.5
- PyTelegramBotApi 4.7.0
- Docker 20.10.12

## Установка
Склонируйте репозиторий 
- ```git clone https://github.com/paragonov/api-parser```

<br>

Создайте файл .env.dev и добавьте следующее
- ```python

  TOKEN='token telegram бота'
  DEBUG=1
  SECRET_KEY='secret key django'
  DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
  SQL_ENGINE=django.db.backends.postgresql
  SQL_DATABASE="название вашей бд"
  SQL_USER="логин пользователя вашей бд"
  SQL_PASSWORD="пароль пользователя вашей бд"
  SQL_HOST=db
  SQL_PORT=5432

  ```
  <br>

Создайте образ docker <br>
- ```docker-compose build```

<br>

Запустите контейнеры <br>
- ```docker-compose up```

<br>

Запустите бота <br>
- ```python3 tg_bot.py```

<br>

Зайдите в бота, напишите команду /start. Бот готов к использованию.
