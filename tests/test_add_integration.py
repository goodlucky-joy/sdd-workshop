from typer.testing import CliRunner


def test_add_integration_creates_todo(tmp_path, monkeypatch):
    from todo_lib.db import create_tables, get_engine
    monkeypatch.setenv("TODO_DB_URL", f"sqlite:///{tmp_path / 'todo.db'}")

    engine = get_engine()
    create_tables(engine=engine)

    from cli.main import app

    runner = CliRunner()
    result = runner.invoke(app, ["add", "Buy milk"])
    assert result.exit_code == 0
    assert "Todo created:" in result.stdout
