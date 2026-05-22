import os
from functools import lru_cache


def _load_local_env_file(path: str = ".env") -> None:
	if not os.path.exists(path):
		return

	with open(path, "r", encoding="utf-8") as env_file:
		for raw_line in env_file:
			line = raw_line.strip()
			if not line or line.startswith("#") or "=" not in line:
				continue

			key, value = line.split("=", 1)
			os.environ.setdefault(key.strip(), value.strip())


_load_local_env_file()


class Settings:
	def __init__(self) -> None:
		self.imagekit_private_key = os.getenv("IMAGEKIT_PRIVATE_KEY", "")
		self.imagekit_public_key = os.getenv("IMAGEKIT_PUBLIC_KEY", "")
		self.imagekit_url = os.getenv("IMAGEKIT_URL", "")
		self.database_url = os.getenv("DATABASE_URL", "sqlite:///./database.db")


@lru_cache
def get_settings() -> Settings:
	return Settings()


settings = get_settings()

IMAGEKIT_PRIVATE_KEY = settings.imagekit_private_key
IMAGEKIT_PUBLIC_KEY = settings.imagekit_public_key
IMAGEKIT_URL = settings.imagekit_url
