# tests/test_env_access.py
from api.core.config import Settings, get_settings

def test_env_settings():
    s = Settings()
    assert s.mail_domain        # czy .env został odczytany
    assert s.redis_url
    assert s.job_ttl > 0

def test_config_cache():
    instance1 = get_settings()
    instance2 = get_settings()
    assert id(instance1) == id(instance2)  # ten sam obiekt w pamięci