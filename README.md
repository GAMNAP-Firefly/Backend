# Fittest Backend

Backend API для системы тестирования Fittest, построенный на FastAPI с использованием Clean Architecture.

## 🏗️ Архитектура

Проект следует принципам Clean Architecture и разделен на слои:

```
src/
├── domain/           # Доменный слой (бизнес-логика)
│   ├── entity/      # Сущности домена
│   └── repository/  # Абстрактные репозитории
├── application/      # Слой приложения
│   ├── dto/         # Data Transfer Objects
│   ├── service/     # Сервисы приложения
│   └── usecase/     # Use Cases (сценарии использования)
├── infrastructure/   # Инфраструктурный слой
│   ├── config/      # Конфигурация
│   ├── db/          # База данных и репозитории
│   ├── services/    # Внешние сервисы
│   └── logging.py   # Логирование
└── presentation/     # Слой представления
    ├── api/         # API контроллеры
    └── schemas/     # Pydantic схемы
```

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.10+
- PostgreSQL
- Docker (опционально)

### Установка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd fittin_backend
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте переменные окружения:**
```bash
cp env.example .env
# Отредактируйте .env файл под ваши настройки
```

5. **Настройте базу данных:**
```bash
# Создайте базу данных PostgreSQL
createdb fittest

# Примените миграции
alembic upgrade head
```

6. **Запустите приложение:**
```bash
# Способ 1: Через скрипт
python run.py

# Способ 2: Напрямую
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker

```bash
# Сборка и запуск с Docker Compose
docker-compose up --build
```

## 📚 API Документация

После запуска приложения документация доступна по адресам:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## 🔐 Аутентификация

API использует JWT токены для аутентификации. Для защищенных эндпоинтов необходимо передавать токен в заголовке:

```
Authorization: Bearer <your-jwt-token>
```

## 📁 Структура проекта

### Domain Layer

- **Entity:** Бизнес-сущности (User, Test, Question, Answer, etc.)
- **Repository:** Абстрактные интерфейсы для доступа к данным

### Application Layer

- **DTO:** Объекты передачи данных между слоями
- **Use Case:** Сценарии использования приложения
- **Service:** Бизнес-логика приложения

### Infrastructure Layer

- **Config:** Настройки приложения через Pydantic Settings
- **Database:** SQLAlchemy модели и репозитории
- **Services:** Внешние сервисы (JWT, логирование)

### Presentation Layer

- **API:** FastAPI роутеры
- **Schemas:** Pydantic схемы для валидации запросов/ответов

## 🛠️ Разработка

### Добавление нового API эндпоинта

1. **Создайте Use Case** в `application/usecase/`
2. **Создайте DTO** в `application/dto/`
3. **Создайте схемы** в `presentation/schemas/`
4. **Создайте контроллер** в `presentation/api/`
5. **Подключите роутер** в `main.py`

### Миграции базы данных

```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Описание изменений"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

### Логирование

Логирование настроено через стандартный модуль `logging`. Уровень логирования можно настроить через переменную окружения `LOG_LEVEL`.

## 🧪 Тестирование

```bash
# Запуск тестов
python -m pytest tests/ -v

# Запуск с покрытием
python -m pytest tests/ --cov=src
```

## 📦 Развертывание

### Production

1. Установите `DEBUG=false` в `.env`
2. Настройте `SECRET_KEY` на безопасное значение
3. Настройте `CORS_ORIGINS` для ваших доменов
4. Настройте логирование в файл

### Docker Production

```bash
docker build -t fittest-backend .
docker run -p 8000:8000 fittest-backend
```

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Добавьте тесты
5. Создайте Pull Request

## 📄 Лицензия

MIT License

## 🆘 Поддержка

Если у вас есть вопросы или проблемы, создайте Issue в репозитории.
