# Используем официальный образ Python
FROM python:3.12.7-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем необходимые системные зависимости
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем poetry
RUN pip install poetry

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock ./

# Устанавливаем зависимости
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копируем код проекта
COPY . .

# Открываем порт
EXPOSE 8000

# Команда для запуска приложения
CMD ["poetry", "run", "python", "src/manage.py", "runserver", "0.0.0.0:8000"]