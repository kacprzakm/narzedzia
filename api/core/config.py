#globalne ustawienia
#nie ma domyslnych wartosci, wiec .env musi istniec
#lru_cache, wartosci sie nie zmieniaja wiec mozna uzyc singletona
#wyjasnienie tutaj: https://www.youtube.com/watch?v=K0Q5twtYxWY
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

#zbieranie ustawien z .env
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    mail_domain: str
    redis_url: str
    job_ttl: int
    cors_origin: str


#cache
@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()