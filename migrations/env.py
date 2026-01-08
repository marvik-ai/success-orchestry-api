import os
import sys

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel

from src.models.employee_model import Employee, EmployeePersonalInfo, EmployeeFinancialInfo

# Ensure the app directory is in the path
sys.path.append(os.getcwd())

load_dotenv()

target_metadata = SQLModel.metadata

# Debugging block to verify registration
print("--- DEBUG: Alembic is looking at these tables in code ---")
print(list(target_metadata.tables.keys()))
print("---------------------------------------------------------")

config = context.config
user = os.getenv('DB_USER', 'postgres')
password = os.getenv('DB_PASSWORD', 'password')
host = os.getenv('DB_HOST', 'localhost')
port = os.getenv('DB_PORT', '5432')
dbname = os.getenv('DB_NAME', 'postgres')

db_url = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
config.set_main_option('sqlalchemy.url', db_url)

def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix='sqlalchemy.',
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
