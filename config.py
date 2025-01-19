from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import List


class Settings(BaseSettings):
    bot_token: SecretStr  # Токен бота
    admin: List[int]  # Список администраторов
    kino_base: int  # ID канала с фильмами

    # Настройки загрузки .env файла
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

# Загружаем конфигурацию
config = Settings()
admin = config.admin
kino_base = config.kino_base