# Data Model: Todo Tags Feature

**Feature**: `002-todo-tags`
**Date**: 2026-05-03

## Overview

The Todo Tags feature extends the existing Todo entity with an optional tags field. Tags are stored as a JSON array of strings in the database, maintaining backward compatibility with existing Todo records.

## Entity: Todo

### Current Schema (Before Changes)
```python
class Todo(Base):
    __tablename__ = "todos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    priority: Mapped[Priority | None] = mapped_column(SqlEnum(Priority), nullable=True)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
```

### Updated Schema (After Changes)
```python
class Todo(Base):
    __tablename__ = "todos"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    priority: Mapped[Priority | None] = mapped_column(SqlEnum(Priority), nullable=True)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    
    # NEW: Tags field for categorization
    tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default_factory=list)
```

## Field Specifications

### Existing Fields
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | `int` | Primary Key, Auto-increment | Unique identifier |
| `title` | `str` | Not null, Max 255 chars | Todo description |
| `due_date` | `date` | Optional | Due date (if set) |
| `priority` | `Priority` | Optional enum | HIGH, MEDIUM, LOW |
| `done` | `bool` | Not null, Default False | Completion status |
| `created_at` | `datetime` | Not null, Default UTC now | Creation timestamp |

### New Field: tags
| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `tags` | `list[str]` | Not null, Default `[]` | List of tag strings |

**Storage**: JSON array in SQLite TEXT column
**Default**: Empty list `[]`
**Validation**: See validation rules below

## Validation Rules

### Tag Validation
Tags must conform to the following rules:

1. **Count Limit**: Maximum 5 tags per Todo
2. **Length Limit**: Each tag ≤ 20 characters
3. **Uniqueness**: No duplicate tags (case-insensitive)
4. **Content**: Non-empty after whitespace trimming
5. **Unicode**: Full Unicode support (Korean, emojis, etc.)

### Validation Function
```python
def validate_tags(tags: list[str]) -> list[str]:
    """
    Validate and normalize a list of tags.
    
    Args:
        tags: Raw tag strings from user input
        
    Returns:
        Normalized list of valid tags
        
    Raises:
        ValueError: If validation fails
    """
    normalized = []
    
    for tag in tags:
        # Trim whitespace
        tag = tag.strip()
        
        # Skip empty tags
        if not tag:
            continue
            
        # Check length
        if len(tag) > 20:
            raise ValueError(f"Tag too long (max 20 chars): '{tag}'")
            
        # Check for duplicates (case-insensitive)
        if tag.lower() in [t.lower() for t in normalized]:
            raise ValueError(f"Duplicate tag: '{tag}'")
            
        normalized.append(tag)
    
    # Check count
    if len(normalized) > 5:
        raise ValueError(f"Too many tags (max 5): {normalized}")
    
    return normalized
```

## Relationships

### No New Relationships
The tags feature is self-contained within the Todo entity. No new database relationships are introduced.

### Existing Relationships
- **Priority Enum**: Maintains existing relationship
- **Database Session**: Uses existing SQLAlchemy session management

## Data Migration

### Strategy: No Migration Required
- **Backward Compatibility**: Existing records automatically get empty `tags` list
- **Forward Compatibility**: New records can have tags populated
- **Database Schema**: SQLite allows adding columns without migration scripts

### Migration Verification
```sql
-- Existing records get default empty array
SELECT id, tags FROM todos WHERE tags IS NULL; -- Should return 0 rows
SELECT id, tags FROM todos LIMIT 5; -- Should show [] for existing records
```

## Query Patterns

### Tag Filtering
```python
# Case-insensitive tag filtering
def filter_by_tag(todos: list[Todo], tag_filter: str) -> list[Todo]:
    """Filter todos by tag (case-insensitive)"""
    if not tag_filter:
        return todos
    
    filter_lower = tag_filter.lower()
    return [
        todo for todo in todos 
        if any(tag.lower() == filter_lower for tag in todo.tags)
    ]
```

### Combined Filtering
```python
# Support multiple filters together
def list_todos(
    session: Session,
    done_filter: bool | None = None,
    priority_filter: Priority | None = None,
    tag_filter: str | None = None
) -> list[Todo]:
    """List todos with optional filters"""
    todos = session.query(Todo).all()
    
    if done_filter is not None:
        todos = [t for t in todos if t.done == done_filter]
    
    if priority_filter is not None:
        todos = [t for t in todos if t.priority == priority_filter]
    
    if tag_filter:
        todos = filter_by_tag(todos, tag_filter)
    
    return todos
```

## Serialization

### JSON Storage Format
```json
{
  "id": 1,
  "title": "Complete project proposal",
  "due_date": "2026-05-10",
  "priority": "HIGH",
  "done": false,
  "created_at": "2026-05-03T10:00:00Z",
  "tags": ["work", "urgent", "meeting"]
}
```

### Display Formatting
```python
def format_todo(todo: Todo) -> str:
    """Format todo for CLI display"""
    if todo.tags:
        tags_str = ", ".join(todo.tags)
        return f"[{tags_str}] {todo.title}"
    return todo.title

# Examples:
# "[work, urgent] Complete project proposal"
# "Buy groceries"  # No tags
```

## Edge Cases

### Empty Tags
- **Input**: `[]` or no `--tag` options
- **Storage**: `[]` (empty JSON array)
- **Display**: No brackets shown

### Unicode Tags
- **Input**: `["작업", "🚀", "café"]`
- **Storage**: Properly stored as Unicode strings
- **Display**: Unicode characters displayed correctly in terminal

### Validation Failures
- **Too many tags**: `ValueError` with descriptive message
- **Duplicate tags**: Case-insensitive detection
- **Long tags**: Length validation with specific error
- **Empty tags**: Filtered out silently

## Performance Characteristics

### Storage
- **Size**: ~2-100 bytes per Todo (depending on tag count)
- **Index**: No additional indexes needed
- **Query**: JSON column queries work efficiently for small datasets

### Filtering
- **Complexity**: O(n*m) where n=todos, m=average tags per todo
- **Optimization**: In-memory filtering acceptable for typical use cases
- **Scalability**: Sufficient for hundreds to thousands of todos

## Testing Considerations

### Unit Tests
- Tag validation function
- Serialization/deserialization
- Filtering logic
- Edge cases (empty, unicode, duplicates)

### Integration Tests
- Database persistence
- CLI command integration
- Combined filtering scenarios

### Sample Test Cases
```python
def test_tag_validation():
    # Valid cases
    assert validate_tags(["work", "urgent"]) == ["work", "urgent"]
    
    # Edge cases
    assert validate_tags(["  work  "]) == ["work"]  # Trimmed
    assert validate_tags([]) == []  # Empty allowed
    
    # Invalid cases
    with pytest.raises(ValueError, match="too long"):
        validate_tags(["this_tag_is_way_too_long_for_validation"])
    
    with pytest.raises(ValueError, match="duplicate"):
        validate_tags(["work", "Work"])  # Case-insensitive duplicate
```

## Schema Evolution

### Future Extensions
- **Tag Categories**: Could extend to typed tags
- **Tag Metadata**: Colors, descriptions, etc.
- **Tag Relationships**: Hierarchical tags

### Backward Compatibility
- Existing API consumers unaffected
- Database schema remains compatible
- CLI interface preserves existing behavior

## Summary

The tags feature adds a simple yet powerful categorization system to Todos:
- **Storage**: JSON array in existing table
- **Validation**: Strict rules prevent bad data
- **Filtering**: Case-insensitive tag matching
- **Display**: Clean bracket notation
- **Compatibility**: Zero breaking changes

This design maintains the project's principles of simplicity and minimal dependencies while adding significant functionality.
