# Dockerfile

# Используем официальный образ Python slim
FROM python:3.11-slim

# Устанавливаем системные зависимости (нужны для сборки некоторых питоновских библиотек)
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем ТОЛЬКО файл зависимостей (это ускорит сборку, если код меняется, а библиотеки - нет)
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь остальной проект в контейнер
COPY . .

# Открываем порт 8000 для доступа к приложению извне контейнера
EXPOSE 8000

# Команда для запуска сервера разработки (Gunicorn лучше для продакшена, но runserver проще для отладки)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]