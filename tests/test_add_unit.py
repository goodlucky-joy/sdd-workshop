import pytest
from todo_lib import add_todo, list_todos
from todo_lib.db import create_tables, get_engine, get_session


def test_add_todo_persists_and_returns_row(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        todo = add_todo("Buy milk", due_date="2026-12-31", priority="High", session=session)

        assert todo.id is not None
        assert todo.title == "Buy milk"
        assert todo.due_date.isoformat() == "2026-12-31"
        assert todo.priority.name == "High"
        assert todo.done is False

        rows = list_todos(session=session)
        assert len(rows) == 1
        assert rows[0].title == "Buy milk"


def test_add_todo_requires_title(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        with pytest.raises(ValueError, match="Title is required"):
            add_todo("", session=session)


def test_add_todo_invalid_due_date(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        with pytest.raises(ValueError, match="Invalid date format"):
            add_todo("Buy milk", due_date="12/31/2026", session=session)
