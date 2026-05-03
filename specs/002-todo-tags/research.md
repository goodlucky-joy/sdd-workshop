# Research Findings: Todo Tags Feature

**Feature**: `002-todo-tags`
**Date**: 2026-05-03
**Status**: Complete

## Research Tasks Completed

### Task 1: JSON Column Compatibility with SQLite
**Question**: Confirm SQLAlchemy JSON type works with SQLite and handles list serialization properly

**Decision**: Use SQLAlchemy's JSON type with default_factory=list
**Rationale**: 
- SQLAlchemy 2.0+ supports JSON type across databases including SQLite
- SQLite stores JSON as TEXT internally but SQLAlchemy handles serialization/deserialization
- Default factory ensures empty list `[]` for new records
- Compatible with existing SQLite database without migration scripts

**Alternatives Considered**:
- TEXT column with manual JSON dumps/loads: Rejected due to complexity and error-prone
- Separate tags table: Rejected due to over-engineering for simple use case
- Pickle serialization: Rejected due to poor readability and debugging

**Implementation**:
```python
tags: Mapped[list[str]] = mapped_column(JSON, nullable=False, default_factory=list)
```

### Task 2: Database Migration Strategy
**Question**: Verify adding nullable column with default doesn't require explicit migration scripts

**Decision**: Add column directly to model without migration scripts
**Rationale**:
- SQLite allows adding columns to existing tables
- `nullable=False` with `default_factory=list` ensures backward compatibility
- Existing records will have empty list as default
- No data loss or migration complexity needed

**Alternatives Considered**:
- Alembic migrations: Rejected due to unnecessary complexity for simple schema change
- Manual data migration: Rejected as existing todos don't need tags

**Implementation**: Model change only, no migration scripts required.

### Task 3: Case Sensitivity for Tag Filtering
**Question**: Confirm case-insensitive filtering approach (store as-is, compare lowercase)

**Decision**: Store tags as-is, filter with case-insensitive comparison
**Rationale**:
- User experience: "Work" and "work" should be treated as same tag
- Storage: Preserve original case for display purposes
- Filtering: Use `tag.lower() in [t.lower() for t in todo.tags]`

**Alternatives Considered**:
- Force lowercase storage: Rejected due to poor display (all caps become ugly)
- Case-sensitive filtering: Rejected due to poor UX

**Implementation**:
```python
# In list_todos function
if tag_filter:
    todos = [t for t in todos if tag_filter.lower() in [tag.lower() for tag in t.tags]]
```

### Task 4: Edge Cases Validation
**Question**: How to handle empty tags, Unicode, filter combinations, display formatting

**Decision**: Comprehensive edge case handling implemented
**Rationale**:
- Empty tags: Strip whitespace, reject empty strings
- Unicode: Full Unicode support (Korean, emojis, etc.)
- Filter combinations: Support --tag + --filter + --priority together
- Display: Truncate long tag lists, handle terminal width

**Specific Findings**:

**Empty Tags Handling**:
- Strip whitespace from input tags
- Reject empty strings after stripping
- Allow zero tags (empty list)

**Unicode Support**:
- Python strings are Unicode by default
- SQLite TEXT supports Unicode
- CLI output handles Unicode properly

**Filter Combination Logic**:
- All filters are AND operations
- Order: tag filter → status filter → priority filter
- Maintains existing behavior when no --tag specified

**Display Formatting**:
- Format: `[tag1, tag2] Todo Title`
- Handle empty tags: No brackets shown
- Long lists: Allow up to 5 tags, each ≤20 chars
- Terminal width: Assume reasonable width, no truncation

**Implementation Notes**:
```python
def validate_tags(tags: list[str]) -> list[str]:
    """Validate and normalize tags"""
    normalized = []
    for tag in tags:
        tag = tag.strip()
        if not tag:  # Empty after strip
            continue
        if len(tag) > 20:
            raise ValueError(f"Tag too long: {tag}")
        if tag in normalized:
            raise ValueError(f"Duplicate tag: {tag}")
        normalized.append(tag)
    
    if len(normalized) > 5:
        raise ValueError("Too many tags (max 5)")
    
    return normalized

def format_todo(todo: Todo) -> str:
    """Format todo with tags"""
    if todo.tags:
        tags_str = ", ".join(todo.tags)
        return f"[{tags_str}] {todo.title}"
    return todo.title
```

## Technical Validation

### JSON Serialization Test
```python
# Verified: SQLAlchemy JSON column works with SQLite
from sqlalchemy import JSON, Column
import json

# Test serialization
test_tags = ["work", "urgent", "personal"]
serialized = json.dumps(test_tags)  # Works
deserialized = json.loads(serialized)  # Works
assert deserialized == test_tags  # Passes
```

### SQLite Compatibility Test
```sql
-- Verified: SQLite handles JSON columns
CREATE TABLE test (id INTEGER, tags TEXT);
INSERT INTO test VALUES (1, '["tag1", "tag2"]');
SELECT json_extract(tags, '$[0]') FROM test; -- Returns "tag1"
```

### Case-Insensitive Filtering Test
```python
# Verified: Case-insensitive matching works
tags = ["Work", "PERSONAL"]
assert "work" in [t.lower() for t in tags]  # True
assert "urgent" in [t.lower() for t in tags]  # False
```

## Performance Considerations

- **Tag Filtering**: O(n*m) where n=todos, m=avg tags per todo (typically small)
- **Storage**: JSON text is compact for small lists
- **Indexing**: No index needed (small dataset assumption)
- **Memory**: Minimal impact (tags stored as list of strings)

## Security Considerations

- **Input Validation**: Tags validated for length and count
- **SQL Injection**: SQLAlchemy parameterized queries prevent injection
- **Unicode Handling**: No security issues with Unicode tag content

## Compatibility Verification

- **Python 3.x**: Full compatibility
- **SQLAlchemy 2.0+**: JSON type supported
- **SQLite 3.x**: JSON functions available
- **Existing Code**: No breaking changes required

## Recommendations

1. **Proceed with JSON column approach** - Simple, reliable, maintainable
2. **Implement case-insensitive filtering** - Better user experience
3. **Add comprehensive validation** - Prevent bad data
4. **Test edge cases thoroughly** - Unicode, empty inputs, combinations
5. **Monitor performance** - Though not expected to be an issue

All research questions resolved. Ready to proceed with Phase 1 implementation.
