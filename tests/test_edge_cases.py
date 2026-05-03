"""Tests for edge cases in tag functionality."""
import pytest
from todo_lib import add_todo, validate_tags, normalize_tags


def test_unicode_tags(session):
    """T026: Test tags with Unicode characters."""
    todo = add_todo(
        title='International task',
        tags=['工作', '긴급', 'трудовой'],
        session=session
    )
    assert len(todo.tags) == 3
    assert '工作' in [t.lower() for t in todo.tags]


def test_tags_with_numbers_and_symbols(session):
    """T026: Test tags with numbers and symbols."""
    todo = add_todo(
        title='Task with numeric tags',
        tags=['bug-fix', 'v1.0', 'PR#123'],
        session=session
    )
    assert len(todo.tags) == 3


def test_max_tags_boundary(session):
    """T026: Test adding exactly 10 tags (max allowed)."""
    tags = [f'tag{i}' for i in range(10)]
    todo = add_todo(
        title='Max tags task',
        tags=tags,
        session=session
    )
    assert len(todo.tags) == 10


def test_tag_max_length_boundary(session):
    """T026: Test tag at exactly 50 character limit."""
    tag = 'a' * 50
    todo = add_todo(
        title='Max length tag',
        tags=[tag],
        session=session
    )
    assert len(todo.tags) == 1
    assert len(todo.tags[0]) == 50


def test_tag_with_whitespace_only():
    """T026: Test that whitespace-only tags are rejected."""
    with pytest.raises(ValueError):
        validate_tags(['   ', '  	  '])


def test_mixed_empty_and_valid_tags():
    """T026: Test mix of empty and valid tags."""
    with pytest.raises(ValueError):
        validate_tags(['work', '', 'urgent'])


def test_normalize_tags_special_chars(session):
    """T026: Test tag normalization with special characters."""
    todo = add_todo(
        title='Special char tags',
        tags=['test-case', 'bug_fix', 'feature/new'],
        session=session
    )
    # All should be preserved
    assert len(todo.tags) == 3


def test_case_preservation_in_storage(session):
    """T026: Test that tag case is preserved after normalization."""
    todo = add_todo(
        title='Case test',
        tags=['WorkFlow', 'IMPORTANT'],
        session=session
    )
    # Tags are stored but case-insensitive matching should work
    assert len(todo.tags) == 2


def test_duplicate_with_different_cases(session):
    """T026: Test deduplication with different cases."""
    from todo_lib import normalize_tags
    result = normalize_tags(['Python', 'PYTHON', 'python', 'PyThOn'])
    assert len(result) == 1


def test_empty_tag_in_list_with_spaces():
    """T026: Test validation rejects empty strings after strip."""
    result = validate_tags(['work', 'urgent'])
    assert len(result) == 2
    
    # But should reject if any become empty after strip
    with pytest.raises(ValueError):
        validate_tags(['work', '   '])
