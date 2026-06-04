# Менеджер задач (Task Manager)

Простое, но production-ready приложение для управления задачами на Django  + PostgreSQL + Gunicorn + Nginx.

## Возможности

- Модель Task с полями: название, описание, статус (todo / in_progress / done), приоритет (low / medium / high), срок, дата создания, владелец.
- Регистрация, вход и выход. **Только свои задачи** видны и редактируются.
- Фильтрация по статусу, приоритету + поиск по названию + пагинация.
- Красивый современный UI (Tailwind CDN) + адаптив.
- Полноценный Django Admin с фильтрами, действиями и русским интерфейсом.
- Поддержка статических файлов и медиа через Nginx.
- Полностью контейнеризировано (multi-stage Dockerfile).

## Требования

- Docker + Docker Compose
- (Опционально) Python 3.13+ для локальной разработки без Docker

## Быстрый запуск (Docker Compose)

1. Скопируйте пример окружения:
   ```powershell
   copy .env.example .env
   # или в bash: cp .env.example .env
   ```

2. Отредактируйте `.env`:
   - Сгенерируйте `SECRET_KEY`:
     ```powershell
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - Задайте надёжный `POSTGRES_PASSWORD`

3. Запустите:
   ```powershell
   docker compose up --build -d
   ```

4. Примените миграции и создайте суперпользователя:
   ```powershell
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py createsuperuser
   ```

5. Откройте http://localhost

   - Зарегистрируйтесь или войдите
   - Создавайте, редактируйте, удаляйте задачи
   - Используйте фильтры
   - Зайдите в /admin

Остановить:
```powershell
docker compose down -v
```


## Локальная разработка (без Docker, sqlite)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

(Для Postgres локально отредактируйте DATABASES или используйте .env + переменные.)