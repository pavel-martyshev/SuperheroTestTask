from config import get_config

config = get_config()

TORTOISE_CONFIG = {
    "connections": {
        "default": f"postgres://{config.postgres_user}:{config.postgres_password}@{config.postgres_host}:{config.postgres_port}/{config.postgres_db}"
    },
    "apps": {
        "models": {
            "models": ["database.models.hero", "aerich.models"],
            "default_connection": "default",
        }
    }
}
