# Restful-сервис
В данном репозитории находится Rest API, написанный на Python с использованием FastAPI в качестве веб-фреймворка и SQLAlchemy в качестве ORM
# Деплой сервиса
Сервис декомпозирован и может быть развернуть при помощи команды ```docker-compose up --build```
# Функционал
Сервис предназначен для распределения пользователей для тестирования проектови имеет следующие эндпоинты:
* ```/ping```
  Предназначен для проверки состояния сервиса
  - Тип: GET
  - Ответ: ```{'test': 'ok'}```
********************
* ```/create_user```
  Предназначен для создания нового пользователя
  - Тип: ```POST```
  - Параметры
    + ```login```: string
    + ```password```: string
    + ```domain```: string
    + ```project_id```: UUID
    + ```env```: str
  - Ответ: ```{"user_id": user_id,
            "created_ad": date,
            "login": login,
            "password": password,
            "project_id": UUID,
            "env": env,
            "domain": domain,
            "locktime": 0.0}```
********************
* ```/get_users```
  Предназначен для получения списка пользователей
  - Тип: ```GET```
  - Ответ: ```[{"user_id": ...,
            "created_ad":...,
            "login": ...,
            "password": ...,
            "project_id": ...,
            "env": ...,
            "domain": ...,
            "locktime": ...}]```
********************
* ```/acquire_lock```
  Предназначен для блокировки пользователя - смены статуса занятости
  - Тип: ```POST```
  - Параметры
    + ```user_id```: UUID
  - Ответ: ```{"user": user_id,
              "locktime": timestamp,
              "status": string}```
********************
* ```/release_lock```
  Предназначен для освобождения пользователя - смены статуса занятости
  - Тип: ```POST```
  - Параметры
    + ```user_id```: UUID
  - Ответ: ```{"user": user_id,
              "locktime": 0.0,
              "status": string}```
# Стек технологий
| Компонент   | Инструменты |
|-------------|-----------------|
| API | Python | FastAPI, SQLAlchemy |
| База данных | PostgreSQL |
| Тестирование | PyTest, pytest-asyncio |
| Валидация данных | Pydantic |
| Асинхронность | asyncpg, asyncio|
| Контейнеризация | Docker, docker-compose|
| Установка зависимостей | Poetry |

