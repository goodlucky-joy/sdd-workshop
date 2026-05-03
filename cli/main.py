from __future__ import annotations

import typer
from typer import Option

from todo_lib import add_todo, create_tables, delete_todo, list_todos, mark_todo_done

app = typer.Typer(help="Todo CLI application")
create_tables()


def format_todo(todo):
    status = "[x]" if todo.done else "[ ]"
    due = todo.due_date.isoformat() if todo.due_date else "No due date"
    priority = todo.priority.value if todo.priority else "No priority"
    tags_str = ", ".join(todo.tags) if todo.tags else "No tags"
    return f"{todo.id:>3} {status} {todo.title} | due={due} | priority={priority} | tags={tags_str}"


@app.command("add")
def add(
    title: str = typer.Argument(..., help="Todo title"),
    due: str | None = Option(None, "--due", help="Due date in YYYY-MM-DD"),
    priority: str | None = Option(None, "--priority", help="High, Medium, Low"),
    tag: list[str] | None = Option(None, "--tag", help="Tag for the todo (can specify multiple)"),
):
    try:
        todo = add_todo(title=title, due_date=due, priority=priority, tags=tag)
        typer.echo(f"Todo created: {format_todo(todo)}")
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("list")
def list_items(
    status: str | None = Option(None, "--filter", help="Filter by status: done or pending"),
    priority: str | None = Option(None, "--priority", help="Filter by priority"),
    tag: str | None = Option(None, "--tag", help="Filter by tag (case-insensitive)"),
):
    try:
        todos = list_todos(done=status, priority=priority, tag=tag)
        if not todos:
            typer.echo("No todos found.")
            raise typer.Exit()
        for todo in todos:
            typer.echo(format_todo(todo))
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("done")
def done(id: int = typer.Argument(..., help="ID of the todo to mark done")):
    try:
        todo = mark_todo_done(id)
        typer.echo(f"Todo marked done: {format_todo(todo)}")
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1)


@app.command("delete")
def delete(id: int = typer.Argument(..., help="ID of the todo to delete")):
    try:
        delete_todo(id)
        typer.echo(f"Todo deleted: {id}")
    except ValueError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
