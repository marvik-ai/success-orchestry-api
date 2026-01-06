import os

from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv('ENV', 'local')
    version: str = os.getenv('APP_VERSION', '0.1.0')
    client_key: str = os.getenv('CLIENT_KEY', '')
    client_secret: str = os.getenv('CLIENT_SECRET', '')
    database_url: str = os.getenv(
        'DATABASE_URL',
        'postgresql://USER:password1234@localhost:5432/SampleApi',
    )
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    log_file: str = os.getenv('LOG_FILE', 'logs/app.log')

    @property
    def require_client_auth(self) -> bool:
        return bool(self.client_key and self.client_secret)


settings = Settings()
