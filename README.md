# Videocards parser
Приложение позволяет получить информацию о видеокартах через Telegram бота, по заданным параметрам в фильтрации.

### Технологии:
- Python 3.10
- Django 4.1.1 / Django Rest Framework 3.13.1
- PostgreSQL 14.5
- PyTelegramBotApi 4.7.0
- BeautifulSoup4 4.10.0
- Celery 5.2.7
- Redis 4.3.4
- Docker 20.10.12

## Установка
Склонируйте репозиторий 
- ```git clone https://github.com/paragonov/api-parser```

Создайте образ docker <br>
- ```docker-compose build```

Запустите контейнеры <br>
- ```docker-compose up```

Перейдете в бота @discounter_vc_bot

Функционал:
- Кнопка "Mvideo" показывает все доступные видеокарты по фильтрам магазина "Mvideo"
- Кнопка "DNS" показывает все доступные видеокарты по фильтрам магазина "DNS"
- Кнопка "Citilink" показывает все доступные видеокарты по фильтрам магазина "Citilink"
- Кнопка "ComputerUniverse" показывает все доступные видеокарты по фильтрам магазина "ComputerUniverse"(в данный момент в разработке)

Для остановки приложения используйте
- ```docker-compose down --volumes```
