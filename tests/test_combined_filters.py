"""Tests for combined filters (status + priority + tags)."""
import pytest
from typer.testing import CliRunner
from cli.main import app
from todo_lib import add_todo


runner = CliRunner()


def test_combined_filters_tag_and_status(session):
    """T025: Test combined filter: tag + done status."""
    # Add todos with different tags and statuses
    todo1 = add_todo(
        title='Task 1',
        tags=['work', 'urgent'],
        session=session
    )
    todo2 = add_todo(
        title='Task 2',
        tags=['personal'],
        session=session
    )
    
    # Mark first one as done
    todo1.done = True
    session.add(todo1)
    session.commit()
    
    # List only done items with 'work' tag
    from todo_lib import list_todos
    results = list_todos(done='done', tag='work', session=session)
    assert len(results) == 1
    assert results[0].id == todo1.id


def test_combined_filters_tag_and_priority(session):
    """T025: Test combined filter: tag + priority."""
    from todo_lib import Priority
    
    todo1 = add_todo(
        title='Urgent work task',
        tags=['work'],
        priority='High',
        session=session
    )
    todo2 = add_todo(
        title='Low priority personal task',
        tags=['personal'],
        priority='Low',
        session=session
    )
    
    from todo_lib import list_todos
    results = list_todos(priority='High', tag='work', session=session)
    assert len(results) == 1
    assert results[0].id == todo1.id


def test_combined_filters_all_three(session):
    """T025: Test combined filter: status + priority + tag."""
    from todo_lib import Priority
    
    # Add various todos
    todo1 = add_todo(
        title='Done urgent work',
        tags=['work', 'urgent'],
        priority='High',
        session=session
    )
    todo1.done = True
    session.add(todo1)
    
    todo2 = add_todo(
        title='Pending urgent work',
        tags=['work', 'urgent'],
        priority='High',
        session=session
    )
    
    session.commit()
    
    from todo_lib import list_todos
    # Get only pending urgent work items
    results = list_todos(done='pending', priority='High', tag='urgent', session=session)
    assert len(results) == 1
    assert results[0].id == todo2.id
    assert not results[0].done
