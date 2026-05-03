from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from .models import Base

DEFAULT_DB_FILE = Path("todo.db")


def get_database_url() -> str:
    db_url = os.environ.get("TODO_DB_URL")
    if db_url:
        return db_url
    return f"sqlite:///{DEFAULT_DB_FILE.absolute()}"


def get_engine(db_url: str | None = None):
    if db_url is None:
        db_url = get_database_url()
    return create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        future=True,
    )


def get_session(engine=None):
    if engine is None:
        engine = get_engine()
    session_factory = sessionmaker(bind=engine, autoflush=False, future=True)
    return session_factory()


def create_tables(engine=None):
    if engine is None:
        engine = get_engine()
    Base.metadata.create_all(bind=engine)
    _sync_sqlite_schema(engine)


def _sync_sqlite_schema(engine):
    inspector = inspect(engine)
    if 'todos' not in inspector.get_table_names():
        return

    existing_columns = {col['name'] for col in inspector.get_columns('todos')}
    if 'tags' not in existing_columns:
        with engine.connect() as conn:
            conn.execute(text("ALTER TABLE todos ADD COLUMN tags JSON NOT NULL DEFAULT '[]'"))
            conn.commit()
