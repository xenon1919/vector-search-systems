from pathlib import Path


def clean_text(text: str) -> str:
	return " ".join(text.split()).strip()


def read_text_file(file_path: str) -> str:
	return Path(file_path).read_text(encoding="utf-8")


def to_pgvector(values) -> str:
	return "[" + ",".join(str(float(v)) for v in values) + "]"
