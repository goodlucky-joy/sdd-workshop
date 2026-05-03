from todo_lib import add_todo, list_todos, mark_todo_done
from todo_lib.db import create_tables, get_engine, get_session


def test_list_todos_returns_all_items(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        add_todo("A", session=session)
        add_todo("B", session=session)
        todos = list_todos(session=session)

        assert len(todos) == 2


def test_list_todos_filters_done_and_pending(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        add_todo("A", session=session)
        todo = add_todo("B", session=session)
        mark_todo_done(todo.id, session=session)

        done_items = list_todos(done="done", session=session)
        pending_items = list_todos(done="pending", session=session)

        assert len(done_items) == 1
        assert done_items[0].done is True
        assert len(pending_items) == 1
        assert pending_items[0].done is False


def test_list_todos_filters_priority(tmp_path, monkeypatch):
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")
    engine = get_engine()
    create_tables(engine=engine)

    with get_session(engine) as session:
        add_todo("A", priority="High", session=session)
        add_todo("B", priority="Low", session=session)
        priority_items = list_todos(priority="High", session=session)

        assert len(priority_items) == 1
        assert priority_items[0].priority.name == "High"
