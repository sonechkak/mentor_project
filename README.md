# Руководство по настройке проекта

## Необходимые условия ⚙️
* Docker
* Docker Compose
* Git

## Начало работы 🚀

### 1. Настройка окружения 🔑
Создай `.env` файл в корневом каталоге по примеру `.env.example`:
```env
# Настройка БД
DB_NAME=mentor_app
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db

# Настройки Django
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 3. Настройка Docker 🐋
Соберите и запустите контейнеры:
```bash
# Собрать и запустить контейнеры
docker compose up --build -d

# Применить миграции
docker compose exec web python src/manage.py migrate

# Создать администратора
docker compose exec web python src/manage.py createsuperuser
```

## Точки доступа 🌐
* **Django App**: [http://localhost:8000](http://localhost:8000)
* **Admin Panel**: [http://localhost:8000/admin](http://localhost:8000/admin)
* **Database**: Port 5432

## Структура проекта 📁
```
sysmind_mentor_proj/
├── src/                # директория с кодом
│   ├── apps/           # наши апки
│   │   ├── accounts/
│   │   └── blog/
│   ├── config/         # базовые настройки типа wsgi и asgi, urls основной
│   ├── settings/       # базовые настройки Django
│   └── manage.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Полезные команды 💻

### Управление Docker
```bash
# Запустить сервисы
docker compose up -d

# Остановить сервисы
docker compose down

# Посмотреть логи
docker compose logs -f

# Перезапустить сервисы
docker compose restart
```
## Устранение неполадок 🔧

### Распространенные проблемы
1. **Конфликты портов**
   * Проверьте, что порты 8000 и 5432 доступны 
   * При необходимости измените порты в docker-compose.yml
   * Убедитесь, что вы в принципе запустили приложение Docker фоном

2. **Подключение к базе данных**
   * Убедитесь, что контейнер базы данных работает
   * Проверьте credentials в .env файле
   * Убедитесь, что правильно передает хост базы данных, тип данных int

3. **Проблемы с контейнерами**
   ```bash
   # Проверить статус контейнеров
   docker compose ps
   
   # Посмотреть логи контейнеров
   docker compose logs
   ```

## Разработка 🛠️

### Требования

* Poetry
* python=3.12.7

```bash
poetry install --with dev 
```

Эта команда запускает установку инструментов разработчика? таких как flake8, black, pytest

Запуск инструментов разработчика

```bash
poetry run pytest src/tests/../tests.py
poetry run flake8 src
poetry run black src
```

### Миграции
```bash
# Применить миграции
python src/manage.py migrate
```

### Запуск сервера и отладка
```bash
# Запустить сервер
# По умолчанию доступен по адресу http://127.0.0.1:8000
python src/manage.py runserver
```

## Лицензия 📄
Проект лицензирован согласно MIT License - подробности см. в файле LICENSE.md
