import os

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv('ENV', 'local')
    version: str = os.getenv('APP_VERSION', '0.1.0')
    client_key: str = os.getenv('CLIENT_KEY', '')
    client_secret: str = os.getenv('CLIENT_SECRET', '')
    db_user: str = os.getenv('DB_USER', 'USER')
    db_password: str = os.getenv('DB_PASSWORD', 'password1234')
    db_host: str = os.getenv('DB_HOST', 'localhost')  # Por defecto localhost (para tu PC)
    db_port: str = os.getenv('DB_PORT', '5432')
    db_name: str = os.getenv('DB_NAME', 'SampleApi')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    log_file: str = os.getenv('LOG_FILE', 'logs/app.log')

    @property
    def require_client_auth(self) -> bool:
        return bool(self.client_key and self.client_secret)

    @property
    def database_url(self) -> str:
        return f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}'


settings = Settings()
