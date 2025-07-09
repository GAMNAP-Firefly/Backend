import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Добавляем src в sys.path для корректного импорта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..')))

from src.infrastructure.config.settings import settings
from src.infrastructure.db.models import (
    answer_model, category_model, question_model, result_model, test_model, user_model, variant_model
)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Устанавливаем строку подключения из settings.py
config.set_main_option("sqlalchemy.url", settings.database_url)

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Собираем все метаданные моделей
from sqlalchemy import MetaData

metadata_obj = MetaData()
for mdl in [
    answer_model,
    category_model,
    question_model,
    result_model,
    test_model,
    user_model,
    variant_model
]:
    if hasattr(mdl, 'Base') and hasattr(mdl.Base, 'metadata'):
        for t in mdl.Base.metadata.tables.values():
            if t not in metadata_obj.tables.values():
                metadata_obj._add_table(t.name, t.schema, t)

# Для автогенерации миграций
# Если все модели используют один Base, можно просто target_metadata = Base.metadata
# Здесь собираем вручную, если разные Base

target_metadata = metadata_obj


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
