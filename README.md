# Сервис планировщик

## Структура

- [actions](actions/scheduler_action.py) - Экшен для использования сервиса
- [app](app) - FastAPI сервис планировщик
- [migrations](migrations) - Миграции для БД
- [tests](tests) - Тесты

## Особенности

- Есть тестовая оберка в [докер](docker-compose.yml) с метриками
- Используется простая sqlite3 база, в корне проекта

## Использование

### Планировщик

- Клонировать `git clone https://git.promo-bot.ru/v.merkurev/nc-scheduler.git`
- Установить зависимости `poetry install`
- Запустить `poetry run python main.py`

### Экшен

#### Переменные

- action: Действие
- mobile_phone: Идентификатор пользователя
- dance: Описание
- date: Дата

Переменные можно изменить в классе [Constants](actions/scheduler_action.py)

#### send

Запись в таблицу

#### get_by_user

Чтение из таблицы записей по номеру телефона
