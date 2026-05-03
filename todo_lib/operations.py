from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import get_session
from .models import Priority, Todo


def parse_due_date(value: str | None) -> datetime.date | None:
    if value is None or value.strip() == "":
        return None
    try:
        return datetime.strptime(value.strip(), "%Y-%m-%d").date()
    except ValueError as exc:
        raise ValueError("Invalid date format") from exc


def parse_priority(value: str | None) -> Priority | None:
    if value is None or value.strip() == "":
        return None
    normalized = value.strip().capitalize()
    try:
        return Priority[normalized]
    except KeyError as exc:
        raise ValueError("Priority must be High, Medium, or Low") from exc


def add_todo(
    title: str,
    due_date: str | None = None,
    priority: str | None = None,
    session: Session | None = None,
) -> Todo:
    if not title or not title.strip():
        raise ValueError("Title is required")

    due = parse_due_date(due_date)
    priority_enum = parse_priority(priority)

    own_session = False
    if session is None:
        session = get_session()
        own_session = True

    try:
        todo = Todo(title=title.strip(), due_date=due, priority=priority_enum)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo
    finally:
        if own_session:
            session.close()


def list_todos(
    done: str | None = None,
    priority: str | None = None,
    session: Session | None = None,
) -> list[Todo]:
    own_session = False
    if session is None:
        session = get_session()
        own_session = True

    try:
        query = select(Todo).order_by(Todo.created_at.asc())

        if done is not None:
            status = done.strip().lower()
            if status == "done":
                query = query.where(Todo.done.is_(True))
            elif status == "pending":
                query = query.where(Todo.done.is_(False))
            else:
                raise ValueError("Filter must be done or pending")

        if priority is not None and priority.strip() != "":
            priority_enum = parse_priority(priority)
            query = query.where(Todo.priority == priority_enum)

        return session.execute(query).scalars().all()
    finally:
        if own_session:
            session.close()


def mark_todo_done(todo_id: int, session: Session | None = None) -> Todo:
    own_session = False
    if session is None:
        session = get_session()
        own_session = True

    try:
        todo = session.get(Todo, todo_id)
        if todo is None:
            raise ValueError("Todo item not found")

        if not todo.done:
            todo.done = True
            session.add(todo)
            session.commit()
            session.refresh(todo)

        return todo
    finally:
        if own_session:
            session.close()


def delete_todo(todo_id: int, session: Session | None = None) -> None:
    own_session = False
    if session is None:
        session = get_session()
        own_session = True

    try:
        todo = session.get(Todo, todo_id)
        if todo is None:
            raise ValueError("Todo item not found")

        session.delete(todo)
        session.commit()
    finally:
        if own_session:
            session.close()
