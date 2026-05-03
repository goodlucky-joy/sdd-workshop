# Implementation Plan: Todo Tags Feature

**Feature**: `002-todo-tags`
**Created**: 2026-05-03
**Status**: Planning
**Branch**: `002-todo-tags`

## Technical Context

### Current Architecture
- **Language**: Python 3.x
- **Framework**: Typer (CLI), SQLAlchemy (ORM)
- **Database**: SQLite
- **Testing**: pytest
- **Code Structure**:
  - `todo_lib/models.py`: SQLAlchemy models
  - `todo_lib/operations.py`: Business logic functions
  - `cli/main.py`: CLI commands using Typer
  - `tests/`: Unit and integration tests

### Existing Todo Model
```python
class Todo(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    priority: Mapped[Priority | None] = mapped_column(SqlEnum(Priority), nullable=True)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
```

### Feature Requirements Summary
- Add optional tags (0-5 tags, each ≤20 chars) to Todo items
- Store tags as JSON array in database
- CLI input: `todo add "title" --tag tag1 --tag tag2`
- CLI output: `[tag1, tag2] title` for tagged todos
- Filter: `todo list --tag tagname` (case-insensitive)
- Preserve all existing functionality
- Maintain backward compatibility

## Implementation Plan

### Phase 1: Data Model Changes
**Goal**: Extend Todo model to support tags without breaking existing data

1. **Database Migration Strategy**
   - Add `tags` column as JSON type to existing `todos` table
   - Use SQLAlchemy's `JSON` type for cross-database compatibility
   - Default value: empty list `[]`
   - No data migration needed (new column starts empty)

2. **Model Updates**
   - Add `tags: Mapped[list[str]]` field to Todo model
   - Use `mapped_column(JSON, nullable=False, default=list)` 
   - Ensure JSON serialization/deserialization works correctly

### Phase 2: Business Logic Updates
**Goal**: Add tag validation and filtering logic to operations.py

1. **Tag Validation Functions**
   - `validate_tags(tags: list[str]) -> list[str]`: Check count (≤5), length (≤20), uniqueness
   - `normalize_tags(tags: list[str]) -> list[str]`: Trim whitespace, handle case sensitivity

2. **Operations Updates**
   - Modify `add_todo()` to accept `tags` parameter
   - Modify `list_todos()` to accept `tag_filter` parameter
   - Add case-insensitive tag matching logic
   - Preserve all existing function signatures for backward compatibility

### Phase 3: CLI Updates
**Goal**: Add --tag options to add and list commands

1. **Add Command Updates**
   - Add `--tag` option (multiple allowed)
   - Pass tags to `add_todo()` function
   - Update help text and validation messages

2. **List Command Updates**
   - Add `--tag` option for filtering
   - Update output formatting to show tags
   - Maintain existing filter compatibility

3. **Output Formatting**
   - Modify `format_todo()` to display tags when present
   - Format: `[tag1, tag2] Todo Title`

### Phase 4: Testing & Validation
**Goal**: Ensure feature works and doesn't break existing functionality

1. **Unit Tests**
   - Test tag validation functions
   - Test model serialization/deserialization
   - Test filtering logic

2. **Integration Tests**
   - Test CLI commands with tags
   - Test combined filters (--tag + --filter)
   - Test edge cases (max tags, duplicates, long tags)

3. **Regression Tests**
   - Run all existing tests to ensure no breakage
   - Test existing CLI commands without tags

## Tasks

### Task 1: Database Schema Update (Priority: P1)
**Description**: Add tags column to Todo model
**Files**: `todo_lib/models.py`
**Effort**: 1-2 hours
**Acceptance Criteria**:
- Todo model has tags field as JSON list
- Database schema includes tags column
- Existing data remains intact

### Task 2: Tag Validation Logic (Priority: P1)
**Description**: Implement tag validation functions
**Files**: `todo_lib/operations.py`
**Effort**: 2-3 hours
**Acceptance Criteria**:
- Validates max 5 tags
- Validates each tag ≤20 characters
- Prevents duplicate tags
- Handles whitespace trimming

### Task 3: Business Logic Updates (Priority: P1)
**Description**: Update add_todo and list_todos functions
**Files**: `todo_lib/operations.py`
**Effort**: 3-4 hours
**Acceptance Criteria**:
- add_todo accepts tags parameter
- list_todos supports tag filtering
- Case-insensitive tag matching
- Backward compatibility maintained

### Task 4: CLI Add Command Update (Priority: P2)
**Description**: Add --tag option to add command
**Files**: `cli/main.py`
**Effort**: 2-3 hours
**Acceptance Criteria**:
- --tag option accepts multiple values
- Tags passed to add_todo function
- Error handling for validation failures

### Task 5: CLI List Command Update (Priority: P2)
**Description**: Add --tag filter and update output formatting
**Files**: `cli/main.py`
**Effort**: 2-3 hours
**Acceptance Criteria**:
- --tag filter option works
- Output shows tags in brackets
- Compatible with existing filters

### Task 6: Unit Tests (Priority: P2)
**Description**: Add tests for tag functionality
**Files**: `tests/test_*.py`
**Effort**: 4-5 hours
**Acceptance Criteria**:
- Tag validation tests
- Model serialization tests
- Filtering logic tests
- All tests pass

### Task 7: Integration Tests (Priority: P3)
**Description**: Test end-to-end CLI functionality
**Files**: `tests/test_*.py`
**Effort**: 3-4 hours
**Acceptance Criteria**:
- CLI commands work with tags
- Combined filters work
- Edge cases handled properly

### Task 8: Regression Testing (Priority: P1)
**Description**: Ensure existing functionality still works
**Files**: All test files
**Effort**: 2-3 hours
**Acceptance Criteria**:
- All existing tests pass
- No breaking changes to existing CLI
- Backward compatibility verified

## Research & Clarification Needed

### Technical Questions
1. **JSON Column Compatibility**: Confirm SQLAlchemy JSON type works with SQLite and handles list serialization properly
2. **Migration Strategy**: Verify adding nullable column with default doesn't require explicit migration scripts
3. **Case Sensitivity**: Confirm case-insensitive filtering approach (store as-is, compare lowercase)

### Edge Cases to Validate
1. **Empty Tags**: How to handle empty string tags vs None
2. **Unicode Tags**: Korean characters in tags work properly
3. **Filter Combination**: --tag + --filter + --priority all work together
4. **Display Formatting**: Long tag lists don't break terminal output

## Success Criteria

### Functional Success
- [ ] Users can add Todos with 0-5 tags via CLI
- [ ] Tag validation prevents invalid inputs
- [ ] Tag filtering works case-insensitively
- [ ] Output displays tags clearly
- [ ] All existing functionality preserved

### Technical Success
- [ ] No breaking changes to existing code
- [ ] All tests pass (existing + new)
- [ ] Database schema supports tags
- [ ] CLI interface is intuitive

### Quality Success
- [ ] Code follows existing patterns
- [ ] Error messages are clear
- [ ] Edge cases handled gracefully
- [ ] Documentation updated

## Assumptions & Constraints

- **Scope**: Only single tag filtering required (no multi-tag AND/OR logic)
- **Storage**: JSON column approach acceptable for simplicity
- **Performance**: Tag filtering on small datasets (no indexing needed)
- **UI**: Terminal-based CLI only (no web interface)
- **Dependencies**: No new external dependencies allowed

## Risk Assessment

### High Risk
- **Database Schema Changes**: Could break existing data if migration fails
- **Backward Compatibility**: Existing CLI usage must continue working

### Medium Risk
- **JSON Serialization**: SQLite JSON handling might have quirks
- **Filter Logic**: Complex AND logic between multiple filters

### Mitigation Strategies
- **Testing**: Comprehensive test coverage before/after changes
- **Gradual Rollout**: Test schema changes on copy first
- **Fallback**: Ensure old CLI commands work without modification

## Timeline Estimate

- **Phase 1 (Data Model)**: 2-3 hours
- **Phase 2 (Business Logic)**: 4-5 hours  
- **Phase 3 (CLI Updates)**: 4-5 hours
- **Phase 4 (Testing)**: 6-8 hours
- **Total**: 16-21 hours

## Next Steps

1. Start with Task 1 (Database Schema) - lowest risk, foundational
2. Implement Task 2 (Validation) - core business logic
3. Update Task 3 (Operations) - integrate with existing functions
4. Test early and often to catch integration issues
5. Complete CLI updates and comprehensive testing

Ready to proceed with implementation following this plan.
