import pytest
from todo_lib import add_todo, delete_todo, list_todos
from todo_lib.db import create_tables, get_engine, get_session


def test_delete_todo_removes_item(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        todo = add_todo("Delete me", session=session)
        delete_todo(todo.id, session=session)
        todos = list_todos(session=session)

        assert len(todos) == 0


def test_delete_todo_invalid_id_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        with pytest.raises(ValueError, match="Todo item not found"):
            delete_todo(999, session=session)
