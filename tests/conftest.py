from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def isolate_todo_db(tmp_path, monkeypatch):
    db_file = tmp_path / "todo.db"
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{db_file}")
    yield
