"""Tests for tag validation and filtering in operations module."""
import pytest
from todo_lib import validate_tags, normalize_tags
from todo_lib.operations import add_todo


def test_validate_tags_valid_tags():
    """T019: Test tag validation with valid tags."""
    result = validate_tags(['work', 'urgent'])
    assert result == ['work', 'urgent']


def test_validate_tags_none():
    """T019: Test tag validation with None."""
    result = validate_tags(None)
    assert result == []


def test_validate_tags_empty_list():
    """T019: Test tag validation with empty list."""
    result = validate_tags([])
    assert result == []


def test_validate_tags_exceeds_max_count():
    """T019: Test tag validation with too many tags."""
    too_many = ['tag' + str(i) for i in range(11)]
    with pytest.raises(ValueError, match="Maximum 10 tags"):
        validate_tags(too_many)


def test_validate_tags_empty_string():
    """T019: Test tag validation with empty string."""
    with pytest.raises(ValueError, match="empty"):
        validate_tags([''])


def test_validate_tags_non_string():
    """T019: Test tag validation with non-string."""
    with pytest.raises(ValueError, match="must be a string"):
        validate_tags([123])


def test_validate_tags_too_long():
    """T019: Test tag validation with tag longer than 50 chars."""
    long_tag = 'a' * 51
    with pytest.raises(ValueError, match="50 characters"):
        validate_tags([long_tag])


def test_normalize_tags_duplicates():
    """T020: Test tag normalization removes case-insensitive duplicates."""
    result = normalize_tags(['Work', 'work', 'WORK'])
    assert len(result) == 1
    assert result[0] in ['Work', 'work', 'WORK']


def test_normalize_tags_trims():
    """T020: Test tag normalization trims whitespace."""
    result = normalize_tags(['  work  ', '  urgent  '])
    # Should trim and sort case-insensitive (preserves first occurrence case)
    assert len(result) == 2
    lower_result = sorted([t.lower() for t in result])
    assert lower_result == ['urgent', 'work']


def test_normalize_tags_none():
    """T020: Test tag normalization with None."""
    result = normalize_tags(None)
    assert result == []


def test_normalize_tags_empty_list():
    """T020: Test tag normalization with empty list."""
    result = normalize_tags([])
    assert result == []


def test_normalize_tags_deduplicates_sorted():
    """T020: Test that normalization deduplicates and sorts case-insensitively."""
    result = normalize_tags(['zebra', 'Apple', 'BANANA', 'apple'])
    # Should be case-insensitively unique and sorted
    assert len(result) == 3
    # Check case-insensitive uniqueness and sorting
    lower_tags = [t.lower() for t in result]
    assert lower_tags == sorted(lower_tags)


def test_add_todo_with_tags(session):
    """T021: Test adding todo with tags (model serialization)."""
    todo = add_todo(
        title='Buy milk',
        tags=['shopping', 'urgent'],
        session=session
    )
    # Tags are normalized (deduplicated and sorted case-insensitively)
    assert len(todo.tags) == 2
    assert set(t.lower() for t in todo.tags) == {'shopping', 'urgent'}
    # Check they're sorted
    assert [t.lower() for t in todo.tags] == sorted(t.lower() for t in todo.tags)


def test_tag_filtering_case_insensitive():
    """T022: Test case-insensitive tag filtering (needs live DB)."""
    # This will be tested in integration tests
    pass


def test_backward_compat_add_todo_without_tags(session):
    """T013: Test backward compatibility - add_todo without tags parameter."""
    todo = add_todo(
        title='Clean house',
        session=session
    )
    assert todo.tags == []


def test_backward_compat_add_todo_with_title_only(session):
    """T013: Test backward compatibility - minimal parameters."""
    todo = add_todo(title='Test', session=session)
    assert todo.tags == []
    assert todo.title == 'Test'
