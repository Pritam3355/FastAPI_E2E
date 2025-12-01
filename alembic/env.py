from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
import os
from dotenv import load_dotenv

from app.user.controller import Base
from app.core.config import settings

# Load .env file
load_dotenv()

config = context.config

# Override the sqlalchemy.url from environment
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Or construct it manually from env vars:
# db_url = f"postgresql+psycopg2://<username>:<passwd>@<hostname>:<port>/<db_name>"
# config.set_main_option("sqlalchemy.url", db_url)

fileConfig(config.config_file_name) # pyright: ignore[reportArgumentType]
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section), # pyright: ignore[reportArgumentType]
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()