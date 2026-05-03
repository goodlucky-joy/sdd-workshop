import pytest
from todo_lib import add_todo, mark_todo_done
from todo_lib.db import create_tables, get_engine, get_session


def test_mark_todo_done_changes_status(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        todo = add_todo("Finish task", session=session)
        updated = mark_todo_done(todo.id, session=session)

        assert updated.done is True


def test_mark_todo_done_invalid_id_raises(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        with pytest.raises(ValueError, match="Todo item not found"):
            mark_todo_done(999, session=session)
