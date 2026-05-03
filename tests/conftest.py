from pathlib import Path

import pytest

from todo_lib.db import create_tables, get_engine, get_session


@pytest.fixture(autouse=True)
def isolate_todo_db(tmp_path, monkeypatch):
    db_file = tmp_path / "todo.db"
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{db_file}")
    yield


@pytest.fixture
def session(isolate_todo_db):
    """Provide a test database session."""
    engine = get_engine()
    create_tables(engine)
    session = get_session(engine)
    yield session
    session.close()
