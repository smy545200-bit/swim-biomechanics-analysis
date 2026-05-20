import sqlite3
from pathlib import Path

DEFAULT_DB_PATH = "data/swim_biomech.sqlite3"


def init_db(db_path: str = DEFAULT_DB_PATH, schema_path: str = "database/schema.sql") -> None:
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        schema = Path(schema_path).read_text(encoding="utf-8")
        conn.executescript(schema)
        conn.commit()


def get_connection(db_path: str = DEFAULT_DB_PATH):
    return sqlite3.connect(db_path)
