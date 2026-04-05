import os
from dataclasses import dataclass

try:
	from dotenv import load_dotenv

	load_dotenv()
except ImportError:
	# dotenv is optional; environment variables can still be provided by OS/shell.
	pass


def _get_env(name: str, default: str | None = None, required: bool = False) -> str:
	value = os.getenv(name, default)
	if required and (value is None or value.strip() == ""):
		raise ValueError(f"Missing required environment variable: {name}")
	return value or ""


@dataclass(frozen=True)
class Settings:
	db_name: str
	db_user: str
	db_password: str
	db_host: str
	db_port: int
	gemini_api_key: str
	gemini_model: str
	embedding_model: str
	embedding_dimension: int


settings = Settings(
	db_name=_get_env("DB_NAME", "rag_db"),
	db_user=_get_env("DB_USER", "postgres"),
	db_password=_get_env("DB_PASSWORD", "postgres"),
	db_host=_get_env("DB_HOST", "localhost"),
	db_port=int(_get_env("DB_PORT", "5432")),
	gemini_api_key=_get_env("GEMINI_API_KEY", ""),
	gemini_model=_get_env("GEMINI_MODEL", "gemini-3.1-pro-latest"),
	embedding_model=_get_env("EMBEDDING_MODEL", "all-MiniLM-L6-v2"),
	embedding_dimension=int(_get_env("EMBEDDING_DIM", "384")),
)
