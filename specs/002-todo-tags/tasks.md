# Tasks: Todo Tags Feature

**Feature**: `002-todo-tags`
**Input**: Design documents from `/specs/002-todo-tags/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-contract.md
**Created**: 2026-05-03

**Tests**: Unit and integration tests included as requested in feature specification.

**Organization**: Tasks organized by implementation phase with regression testing as first checkpoint.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 (Todo Tags feature)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Ensure development environment is ready and existing functionality works

- [ ] T001 Run existing test suite to establish baseline
- [ ] T002 Verify current database schema and data integrity
- [ ] T003 Confirm CLI commands work without tags (regression test)

**Checkpoint**: All existing tests pass - ready to implement tags feature

---

## Phase 2: Foundational (Data Model)

**Purpose**: Database schema changes that enable tag functionality

**⚠️ CRITICAL**: Schema changes must be backward compatible

- [ ] T004 [P] [US1] Add tags field to Todo model in todo_lib/models.py
- [ ] T005 [P] [US1] Update database schema with JSON tags column
- [ ] T006 [P] [US1] Test model serialization/deserialization with tags
- [ ] T007 [US1] Verify existing data remains intact after schema change

**Checkpoint**: Database schema supports tags without breaking existing data

---

## Phase 3: Core Business Logic (Tag Operations)

**Purpose**: Tag validation and filtering logic

- [ ] T008 [P] [US1] Implement validate_tags function in todo_lib/operations.py
- [ ] T009 [P] [US1] Add tag normalization logic (trim, deduplicate)
- [ ] T010 [P] [US1] Update add_todo function to accept tags parameter
- [ ] T011 [P] [US1] Update list_todos function to support tag filtering
- [ ] T012 [US1] Implement case-insensitive tag matching logic
- [ ] T013 [US1] Ensure backward compatibility of existing function signatures

**Checkpoint**: Business logic handles tags correctly while preserving existing behavior

---

## Phase 4: CLI Interface (User Commands)

**Purpose**: Add --tag options to CLI commands

- [ ] T014 [P] [US1] Add --tag option to add command in cli/main.py
- [ ] T015 [P] [US1] Add --tag filter option to list command in cli/main.py
- [ ] T016 [P] [US1] Update format_todo function to display tags
- [ ] T017 [US1] Implement error handling for tag validation failures
- [ ] T018 [US1] Update CLI help text and command documentation

**Checkpoint**: CLI accepts tag input and displays tagged todos correctly

---

## Phase 5: Testing & Validation

**Purpose**: Comprehensive testing of tag functionality

### Unit Tests
- [ ] T019 [P] [US1] Test tag validation (count, length, duplicates) in tests/test_operations.py
- [ ] T020 [P] [US1] Test tag normalization and edge cases in tests/test_operations.py
- [ ] T021 [P] [US1] Test model serialization with tags in tests/test_models.py
- [ ] T022 [P] [US1] Test tag filtering logic in tests/test_operations.py

### Integration Tests
- [ ] T023 [P] [US1] Test CLI add command with tags in tests/test_add_integration.py
- [ ] T024 [P] [US1] Test CLI list command with tag filtering in tests/test_list_integration.py
- [ ] T025 [P] [US1] Test combined filters (--tag + --filter + --priority) in tests/test_combined_filters.py
- [ ] T026 [P] [US1] Test edge cases (Unicode tags, empty tags, max tags) in tests/test_edge_cases.py

### Regression Tests
- [ ] T027 [US1] Run all existing tests to ensure no regressions
- [ ] T028 [US1] Test existing CLI commands without tags still work
- [ ] T029 [US1] Verify backward compatibility of all existing functionality

**Checkpoint**: All tests pass including new tag tests and existing regression tests

---

## Phase 6: Documentation & Polish

**Purpose**: Final cleanup and documentation updates

- [ ] T030 [P] [US1] Update README.md with tag usage examples
- [ ] T031 [P] [US1] Add tag examples to quickstart.md validation
- [ ] T032 [US1] Code cleanup and final refactoring
- [ ] T033 [US1] Performance verification (no significant impact on existing operations)

**Checkpoint**: Feature complete and documented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - run first to establish baseline
- **Foundational (Phase 2)**: Depends on Setup - schema changes
- **Core Business Logic (Phase 3)**: Depends on Foundational - needs schema
- **CLI Interface (Phase 4)**: Depends on Core Business Logic - needs operations
- **Testing (Phase 5)**: Depends on CLI Interface - tests end-to-end functionality
- **Documentation (Phase 6)**: Depends on Testing - feature must work

### Parallel Opportunities

- All tasks marked [P] can run in parallel within their phase
- Unit tests can run in parallel
- Integration tests can run in parallel
- Documentation tasks can run in parallel

### Critical Path (Sequential)

1. T001 → T002 → T003 (Setup baseline)
2. T004 → T005 → T006 → T007 (Schema changes)
3. T008 → T009 → T010 → T011 → T012 → T013 (Business logic)
4. T014 → T015 → T016 → T017 → T018 (CLI interface)
5. T019-T026 (Testing - can be parallel)
6. T027 → T028 → T029 (Regression testing)
7. T030 → T031 → T032 → T033 (Polish)

---

## Parallel Example: Business Logic Phase

```bash
# Can run these in parallel (different functions in operations.py):
Task: "Implement validate_tags function in todo_lib/operations.py"
Task: "Add tag normalization logic (trim, deduplicate)"
Task: "Update add_todo function to accept tags parameter"
Task: "Update list_todos function to support tag filtering"
```

---

## Implementation Strategy

### MVP First Approach

1. Complete Phase 1: Setup (baseline established)
2. Complete Phase 2: Foundational (schema ready)
3. Complete Phase 3: Core Business Logic (operations ready)
4. Complete Phase 4: CLI Interface (usable feature)
5. **STOP and VALIDATE**: Test basic tag functionality
6. Complete Phase 5: Testing (comprehensive validation)
7. Complete Phase 6: Polish (production ready)

### Testing First

- Write tests before implementation (TDD approach)
- Each task should have corresponding test
- Regression testing after each major change
- All existing tests must pass at every checkpoint

### Risk Mitigation

- Schema changes tested first (Phase 2)
- Backward compatibility verified early (Phase 1, Phase 5)
- CLI interface tested incrementally
- Comprehensive edge case testing

---

## Success Criteria Validation

### Functional Success Checkpoints

- **After Phase 4**: Users can add/list todos with tags via CLI
- **After Phase 5**: Tag validation prevents invalid inputs
- **After Phase 5**: Tag filtering works case-insensitively
- **After Phase 5**: Output displays tags clearly
- **After Phase 5**: All existing functionality preserved

### Technical Success Checkpoints

- **After Phase 2**: Database schema supports tags
- **After Phase 5**: All tests pass (existing + new)
- **After Phase 5**: No breaking changes to existing code
- **After Phase 5**: CLI interface is intuitive

---

## Notes

- [P] tasks = different functions/files, can run in parallel
- [US1] label = Todo Tags user story
- Each phase has clear checkpoint for validation
- Existing test suite must pass before any implementation
- Regression testing integrated throughout process
- Stop at any checkpoint to validate incremental progress
