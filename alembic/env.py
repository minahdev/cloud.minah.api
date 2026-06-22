import os
import sys

from pathlib import Path
from dotenv import load_dotenv


from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

config = context.config

BACKEND_DIR = Path(__file__).resolve().parent.parent  # backend/
APPS_DIR = BACKEND_DIR / "apps"
sys.path.insert(0, str(BACKEND_DIR))
sys.path.insert(0, str(APPS_DIR))

load_dotenv(BACKEND_DIR / ".env")

database_url = os.getenv("DATABASE_URL", "").strip()

if not database_url:
    raise RuntimeError("DATABASE_URL이 backend/.env 에 없습니다.")


# 이미 postgresql+psycopg:// 이면 그대로 사용
if "+psycopg" not in database_url:
    if database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    elif database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+psycopg://", 1)

config.set_main_option("sqlalchemy.url", database_url)

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.


# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
from core.matrix.database_manager import Base  # noqa: E402
from users.app.dtos.user_information_dto import UserInformation  # noqa: F401, E402
from users.app.dtos.user_dto import User  # noqa: F401, E402
from titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelOrm  # noqa: F401, E402
from titanic.adapter.outbound.orm.passenger_jack_trainer_orm import PassengerModel  # noqa: F401, E402
from inbody.adapter.outbound.orm.food_orm import Food  # noqa: F401, E402

target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
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
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
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
