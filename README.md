<div style="text-align: center;">
   <h1 align="center">Чат-бот для трекинга привычек</h1>
</div>

<p align="center">
  <img src="assets/video/Habit-Tracker.gif" alt="Краткий функционал">
</p>

## Описание проекта

Этот проект представляет собой сервис для трекинга привычек с использованием микросервисной архитектуры. Он включает три основных сервиса:

- **api** – Backend-сервис, реализованный на FastAPI, отвечающий за хранение и обработку данных пользователей. 
Также в нем реализованна аутентификация и авторизация пользователей.
- **bot** – Телеграм-бот, через который пользователи могут управлять своими привычками, и трекать их выполнение.
- **notification** – Сервис уведомлений, отвечающий за отправку напоминаний пользователям о необходимости выполнения привычек.

## Функционал

### Телеграм-бот (bot):
- Добавление, удаление, просмотр и редактирование привычек.
- Фиксация выполнения привычек (выполнил/не выполнил).
- Перенос привычки если пользователь выполнил план внедрения привычки (задать кол-во дней можно в переменных окружения).

### Backend (api):
- Аутентификация и авторизация пользователей.
- Хранение и обработка данных о привычках.
- Реализация CRUD-операций для управления привычками.

### Сервис уведомлений (notification):
- Интеграция с телеграм-ботом для доставки сообщений.
- Напоминания о привычках в назначенное время.


## Технологический стек
![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=yellow)
![FastAPI](https://img.shields.io/badge/FastAPI-%F0%9F%9F%A2?logo=fastapi&logoColor=white)
![FastAPI Users](https://img.shields.io/badge/FastAPI_Users-%23009688?logo=fastapi&logoColor=white)
![Swagger](https://img.shields.io/badge/Swagger-API-green?logo=swagger&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17.2-blue?logo=postgresql&logoColor=darkblue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-%23E34F26?logo=sqlalchemy&logoColor=black)
![Alembic](https://img.shields.io/badge/Alembic-%231572B6?logo=sqlalchemy&logoColor=white)
![PyTelegramBotAPI](https://img.shields.io/badge/PyTelegramBotAPI-%230088cc?logo=telegram&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-%230db7ed?logo=docker&logoColor=white)
![Docker-compose](https://img.shields.io/badge/Docker--compose-%230db7ed?logo=docker&logoColor=white)
![Kafka](https://img.shields.io/badge/Kafka-%23000000?logo=apache-kafka&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-%23DC382D?logo=redis&logoColor=white)


## Установка и запуск

### 1. Настройка переменных окружения
Создайте `.env`-файлы для каждого сервиса (`api/.env`, `bot/.env`, `notification/.env`) и добавьте в них соответствующие настройки.
Также необходимо создать `.env`-файл в корне проекта.
#### Пример корневого `.env` файла:
```ini
DB__USER=<your_db_user>
DB__PASSWORD=<your_db_password>
DB__HOST=<your_db_host>
DB__PORT=<your_db_port>
DB__NAME=<your_db_name>

NGROK__AUTHTOKEN=<your_ngrok_authtoken>

TIMEZONE=<your_timezone>
```
**Примечание:** чтобы тг-бот мог взаимодействовать с нашим сервером нам нужно перенастроить вебхук, который должен быть https. 
Я использовал ngrok, при написании данного проекта. А TIMEZONE нужен для корректной отправки уведомлений и написания логов. 
Указывайте то где будет работать телеграмм бот. 

#### Пример `.env` файла для **api**:
```ini
DB__USER=<your_db_user>
DB__PASSWORD=<your_db_password>
DB__HOST=<your_db_host>
DB__PORT=<your_db_port>
DB__NAME=<your_db_name>

ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET=<your_reset_password_token_secret>
ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET=<your_verification_token_secret>

API__SUPERUSER_NAME=<your_superuser_name>
API__SUPERUSER_EMAIL=<your_superuser_email>
API__SUPERUSER_PASSWORD=<your_superuser_password>

REDIS__HOST=<your_redis_host>
REDIS__PORT=<your_redis_port>
REDIS__DB=<your_redis_db>

KAFKA__BROKER=<your_kafka_broker>

NOTIFICATION__TOPIC=<your_notification_topic>
NOTIFICATION__CLIENT_ID=<your_notification_client_id>
NOTIFICATION__HOUR_WE_REMIND=<your_notification_hour>
```
**Примечание:** ACCESS_TOKEN можете сгенерировать командой:
```bash
python -c 'import secrets; print(secrets.token_hex())'
```
Superuser будет создан при первом запуске api. 
NOTIFICATION__HOUR_WE_REMIND - означает время когда мы будем отправлять напоминание в kafka.
Заметьте что в api есть 2 main.py: один для запуска самого api, а другой запускает фоновую задачу для отправки сообщений в kafka. 

#### Пример `.env` файла для **bot**:
```ini
TG__TOKEN=<your_telegram_token>
#TG__WEBHOOK_URL=<your_telegram_webhook_url>  # Будет генерироваться автоматически через NGROK__AUTHTOKEN
TG__CARRY_OVER_COMPLETE_HABITS_DAYS=<your_carry_over_days>
TG__DEBUG_PORT=<your_debug_port>  # Не обязательно (используется для запуска не через docker)

API__URL=<your_api_url>

REDIS__HOST=<your_redis_host>
REDIS__PORT=<your_redis_port>
REDIS__DB=<your_redis_db>
```
**Примечание:** TG__CARRY_OVER_COMPLETE_HABITS_DAYS - количество дней после отметки которых пользователю отправится
поздравление о том, что он успешно внедрил привычку в свою жизнь.

#### Пример `.env` файла для **notification**:
```ini
TG__TOKEN=<your_telegram_token>

KAFKA__BROKER=<your_kafka_broker>

NOTIFICATION__TOPIC=<your_notification_topic>
NOTIFICATION__CLIENT_ID=<your_notification_client_id>
```
**Примечание:** NOTIFICATION__TOPIC обязательно должен быть с таким же названием, что и в api.

***Общее примечание:*** внутри каждого сервиса есть файл config.py обязательно просмотрите его, в некоторых config.py 
есть настройки, которые я решил не задавать в переменных окружения.


### 2. Запуск с помощью Docker-compose

```sh
 docker compose up --build
```


## Разработчик
- Сарбасов Ратмир
- Контакты: ratmir2020.1@gmail.com

