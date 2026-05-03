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





def validate_tags(tags: list[str] | None) -> list[str]:
    """
    Validate and normalize tags.
    - Tags must be non-empty list or None
    - Each tag must be a non-empty string
    - Maximum 10 tags per todo
    - Each tag max 50 characters
    """
    if tags is None:
        return []
    
    if not isinstance(tags, list):
        raise ValueError("Tags must be a list")
    
    if len(tags) > 10:
        raise ValueError("Maximum 10 tags allowed per todo")
    
    validated = []
    for tag in tags:
        if not isinstance(tag, str):
            raise ValueError("Each tag must be a string")
        
        tag = tag.strip()
        if not tag:
            raise ValueError("Tags cannot be empty")
        
        if len(tag) > 50:
            raise ValueError("Each tag must be 50 characters or less")
        
        validated.append(tag)
    
    return validated


def normalize_tags(tags: list[str] | None) -> list[str]:
    """
    Normalize tags: trim, deduplicate, case-insensitive sorting.
    """
    if not tags:
        return []
    
    # Trim each tag
    trimmed = [tag.strip() for tag in tags]
    
    # Remove empty strings
    trimmed = [tag for tag in trimmed if tag]
    
    # Deduplicate (case-insensitive)
    seen = set()
    deduplicated = []
    for tag in trimmed:
        tag_lower = tag.lower()
        if tag_lower not in seen:
            seen.add(tag_lower)
            deduplicated.append(tag)
    
    # Sort for consistency
    deduplicated.sort(key=str.lower)
    
    return deduplicated

def add_todo(
    title: str,
    due_date: str | None = None,
    priority: str | None = None,
    tags: list[str] | None = None,
    session: Session | None = None,
) -> Todo:
    if not title or not title.strip():
        raise ValueError("Title is required")

    due = parse_due_date(due_date)
    priority_enum = parse_priority(priority)
    validated_tags = validate_tags(tags)
    normalized_tags = normalize_tags(validated_tags)

    own_session = False
    if session is None:
        session = get_session()
        own_session = True

    try:
        todo = Todo(
            title=title.strip(),
            due_date=due,
            priority=priority_enum,
            tags=normalized_tags
        )
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
    tag: str | None = None,
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

        results = session.execute(query).scalars().all()
        
        # Filter by tag if provided (case-insensitive)
        if tag is not None and tag.strip() != "":
            tag_lower = tag.strip().lower()
            results = [
                todo for todo in results
                if any(t.lower() == tag_lower for t in todo.tags)
            ]
        
        return results
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
