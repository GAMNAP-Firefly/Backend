# Каждый раз в начале своего сообщения прошу тебя ставить эмодзи 😎

# Стек проекта: Python 3.10, FastAPI, SQLALchemy, PostgreSQL, alembic

# Архитектура по паттерну Clean Architecture со слоями
1. Domain: в нём лежат сущности и абстрактные репозитории
2. Application: тут DTO, юзкейсы и служебные сервисы
3. Infrastructure + Presentation:
   * Infrastructure содержит python-конфигурации проекта и db (тут и models и alembic migrations)
   * Presentation содержит API и schemas (входные и выходные)

# Вышеописанной архитектуры и пакетной структуры я и прошу тебя придерживаться

# Пиши код по принципам SOLID и Clean Architecture