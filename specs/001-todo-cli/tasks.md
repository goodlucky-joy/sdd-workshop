# Tasks: Todo CLI 기본 기능

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: `plan.md`, `spec.md`

**TDD Structure**: 각 User Story는 다음 순서를 따릅니다:
1. **Red Phase**: 실패하는 단위 테스트 작성
2. **Green Phase**: 최소 구현으로 테스트 통과
3. **Refactor Phase**: 코드 품질 개선
4. **Integration Phase**: CLI 명령 통합 테스트

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: 프로젝트 초기화와 기본 구조를 만든다.

- [ ] T001 Create `pyproject.toml` with Python 3.12, runtime dependencies (`typer`, `sqlalchemy`), and dev dependencies (`pytest`, `pytest-cov`)
- [ ] T002 Create `uv.lock` by initializing the project with `uv` in the repository root
- [ ] T003 Create `README.md` documenting CLI usage, installation, and commands
- [ ] T004 Create package folder `todo_lib/` and file `todo_lib/__init__.py`
- [ ] T005 Create package folder `cli/` and file `cli/__init__.py`
- [ ] T006 Create test folder `tests/` and base file `tests/__init__.py`
- [ ] T007 [P] Create CLI application skeleton in `cli/main.py` with `typer.Typer()` and command placeholders for `add`, `list`, `done`, `delete`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: 비즈니스 로직과 데이터 계층의 기반을 구축한다. TDD Red 단계: 모든 작업 함수의 테스트 케이스를 먼저 정의한다.

### Foundational Test Infrastructure

- [ ] T008 [P] Create `tests/conftest.py` with pytest fixtures for isolated SQLite test database, session factory, and cleanup hooks

### Foundational Model & Data Layer (Green Phase)

- [ ] T009 Create `todo_lib/models.py` and define `Todo` ORM model with `id`, `title`, `due_date`, `priority`, `done`, `created_at`
- [ ] T010 Create `todo_lib/db.py` and implement SQLite engine creation, session management, and `create_tables()` helper

### Foundational Operations (Red → Green → Refactor)

- [ ] T011 [P] Create `tests/test_operations.py` with unit tests for stubs: `add_todo()`, `list_todos()`, `mark_todo_done()`, `delete_todo()` (all should fail initially)
- [ ] T012 Create `todo_lib/operations.py` and implement operation stubs to pass foundational unit tests in `tests/test_operations.py`
- [ ] T013 [P] Create `cli/main.py` command wiring with stubs that call `todo_lib.operations` for each command

---

## Phase 3: User Story 1 - Todo 추가 및 기본 항목 생성 (Priority: P1) 🎯 MVP

**Goal**: `todo add` 명령으로 제목 필수, 선택적 마감일과 우선순위를 가진 Todo 항목을 추가할 수 있다.

**Independent Test Criteria**: 
- `todo add "Buy milk"` 실행 후 목록에 항목이 생성되는가?
- 마감일과 우선순위가 저장되고 조회되는가?
- 제목 없이 실행하면 에러 메시지가 표시되는가?

### US1 - Red Phase: Unit Tests

- [ ] T014 [P] [US1] Create `tests/test_add_unit.py` with failing pytest cases for:
  - Valid `add_todo(title, due_date, priority)` with correct storage
  - Title validation (required, non-empty)
  - Due date parsing validation (`YYYY-MM-DD` format)
  - Priority validation (`High|Medium|Low`)
  - Persistence to SQLite

### US1 - Green Phase: Implementation

- [ ] T015 [US1] Implement `add_todo()` in `todo_lib/operations.py` with title validation, optional `due_date` parsing on `YYYY-MM-DD`, and `priority` enum handling
- [ ] T016 [US1] Implement database insert logic and verify all unit tests in `tests/test_add_unit.py` pass

### US1 - Refactor Phase

- [ ] T017 [P] [US1] Refactor `add_todo()` for error handling clarity, add docstring, verify test coverage ≥ 90%

### US1 - Integration Phase: CLI Layer

- [ ] T018 [US1] Implement `todo add` command in `cli/main.py` to parse `--due` and `--priority` flags and call `todo_lib.operations.add_todo()`
- [ ] T019 [P] [US1] Create `tests/test_add_integration.py` with CLI integration tests for `todo add` command output and error messages
- [ ] T020 [US1] Update `README.md` with `todo add` usage examples and validation rules

---

## Phase 4: User Story 2 - Todo 목록 조회 및 필터링 (Priority: P1)

**Goal**: `todo list` 명령으로 전체 목록 조회와 완료 상태 및 우선순위 필터링이 가능하다.

**Independent Test Criteria**:
- 여러 Todo 항목 추가 후 `todo list`로 모두 조회되는가?
- `--filter done|pending`으로 필터링되는가?
- `--priority high|medium|low`로 필터링되는가?
- 빈 목록에서 적절한 메시지가 표시되는가?

### US2 - Red Phase: Unit Tests

- [ ] T021 [P] [US2] Create `tests/test_list_unit.py` with failing pytest cases for:
  - `list_todos()` returns all items (empty, single, multiple)
  - Filtering by `done` status (done=True, done=False)
  - Filtering by priority (`High`, `Medium`, `Low`)
  - Combined filtering (status + priority)

### US2 - Green Phase: Implementation

- [ ] T022 [US2] Implement `list_todos(filters)` in `todo_lib/operations.py` with status and priority filtering
- [ ] T023 [US2] Implement SQLite query logic and verify all unit tests in `tests/test_list_unit.py` pass

### US2 - Refactor Phase

- [ ] T024 [P] [US2] Refactor `list_todos()` for query efficiency, add docstring, verify test coverage ≥ 90%

### US2 - Integration Phase: CLI Layer

- [ ] T025 [US2] Implement `todo list` command in `cli/main.py` with `--filter` and `--priority` options
- [ ] T026 [P] [US2] Create `tests/test_list_integration.py` with CLI integration tests for list command output formats
- [ ] T027 [US2] Update `README.md` with `todo list` command examples and filter usage

---

## Phase 5: User Story 3 - Todo 완료 처리 (Priority: P2)

**Goal**: `todo done <id>` 명령으로 항목을 완료 상태로 표시할 수 있다.

**Independent Test Criteria**:
- `todo done <id>`로 항목 상태가 완료로 변경되는가?
- 존재하지 않는 ID로 실행하면 에러가 표시되는가?
- 이미 완료된 항목을 다시 완료로 표시할 수 있는가?

### US3 - Red Phase: Unit Tests

- [ ] T028 [P] [US3] Create `tests/test_done_unit.py` with failing pytest cases for:
  - `mark_todo_done(id)` successfully marks item as done
  - Invalid ID raises appropriate exception
  - Idempotent: marking already-done item again succeeds

### US3 - Green Phase: Implementation

- [ ] T029 [US3] Implement `mark_todo_done()` in `todo_lib/operations.py` with ID validation and status update
- [ ] T030 [US3] Implement database update logic and verify all unit tests in `tests/test_done_unit.py` pass

### US3 - Refactor Phase

- [ ] T031 [P] [US3] Refactor `mark_todo_done()` for error handling, add docstring, verify test coverage ≥ 90%

### US3 - Integration Phase: CLI Layer

- [ ] T032 [US3] Implement `todo done` command in `cli/main.py` to call `mark_todo_done()` and display success/error messages
- [ ] T033 [P] [US3] Create `tests/test_done_integration.py` with CLI integration tests
- [ ] T034 [US3] Update `README.md` with `todo done` command usage and expected output

---

## Phase 6: User Story 4 - Todo 삭제 (Priority: P2)

**Goal**: `todo delete <id>` 명령으로 항목을 삭제할 수 있다.

**Independent Test Criteria**:
- `todo delete <id>`로 항목이 삭제되는가?
- 존재하지 않는 ID로 실행하면 에러가 표시되는가?
- 삭제 후 목록에서 제거되는가?

### US4 - Red Phase: Unit Tests

- [ ] T035 [P] [US4] Create `tests/test_delete_unit.py` with failing pytest cases for:
  - `delete_todo(id)` successfully deletes item
  - Invalid ID raises appropriate exception
  - Item no longer appears in subsequent queries

### US4 - Green Phase: Implementation

- [ ] T036 [US4] Implement `delete_todo()` in `todo_lib/operations.py` with ID validation and deletion logic
- [ ] T037 [US4] Implement database delete query and verify all unit tests in `tests/test_delete_unit.py` pass

### US4 - Refactor Phase

- [ ] T038 [P] [US4] Refactor `delete_todo()` for error handling, add docstring, verify test coverage ≥ 90%

### US4 - Integration Phase: CLI Layer

- [ ] T039 [US4] Implement `todo delete` command in `cli/main.py` to call `delete_todo()` and display success/error messages
- [ ] T040 [P] [US4] Create `tests/test_delete_integration.py` with CLI integration tests
- [ ] T041 [US4] Update `README.md` with `todo delete` command usage and expected output

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 테스트 커버리지 확보, 전체 통합 검증, 문서 완성.

### Test Coverage & Quality

- [ ] T042 [P] Run `pytest` with `pytest-cov` for all tests and achieve ≥ 80% overall coverage
- [ ] T043 [P] Create `tests/test_e2e.py` with end-to-end scenario tests: add → list → done → delete workflow
- [ ] T044 [P] [US1] Create tests for invalid due date format handling in `tests/test_add_unit.py`
- [ ] T045 [P] Verify local persistence across restart: confirm `todo.db` is created and data persists after CLI exit

### Integration & Performance

- [ ] T046 [P] Add performance validation: measure response time for `add`, `list`, `done`, `delete` commands (target: < 500ms per command)
- [ ] T047 [P] Verify `todo_lib/db.py` creates `todo.db` in the local working directory and does not require a server

### Documentation & Final Validation

- [ ] T048 [P] Ensure `README.md` describes installation, command usage, all validation rules, and filter examples clearly
- [ ] T049 [P] Verify all PRs satisfy code review gates: test-first structure, ≥ 80% coverage, TDD compliance

---

## Dependencies & Execution Order

**Critical Path**:
- **Phase 1** → **Phase 2** → **Phase 3 & 4** (parallel) → **Phase 5 & 6** (parallel) → **Phase 7**

**Within Each User Story**:
- Red Phase (tests) → Green Phase (implementation) → Refactor Phase → Integration Phase (CLI)
- Tests must all pass before moving to next phase

### Parallel Opportunities

- **Phase 1**: T004–T007 can run in parallel (distinct files)
- **Phase 2**: T008, T009, T010 can prepare in parallel; T011, T012, T013 follow once data layer exists
- **Per Story**: Red phase tests (T014, T021, T028, T035) can all run in parallel
- **Across Stories**: US1–US2 complete phases in parallel after Phase 2; US3–US4 follow similarly
- **Phase 7**: T042–T049 mostly parallelizable except integration tests require all implementations

### User Story Dependencies

- **US1**: Blocks US2 (list depends on add for test data)
- **US2**: Blocks US3, US4 (done/delete require items from add)
- **US3, US4**: Can proceed in parallel after Phase 2

---

## Test-First Summary (TDD Compliance)

| Phase | Test Type | Task Range | Details |
|-------|-----------|-----------|---------|
| 1 | Setup | — | Infrastructure only |
| 2 | Foundational | T008, T011 | Test database + operation stubs |
| 3 | Unit → Integration | T014–T020 | Red (T014) → Green (T015–T016) → Refactor (T017) → Integration (T018–T019) |
| 4 | Unit → Integration | T021–T027 | Red (T021) → Green (T022–T023) → Refactor (T024) → Integration (T025–T026) |
| 5 | Unit → Integration | T028–T034 | Red (T028) → Green (T029–T030) → Refactor (T031) → Integration (T032–T033) |
| 6 | Unit → Integration | T035–T041 | Red (T035) → Green (T036–T037) → Refactor (T038) → Integration (T039–T040) |
| 7 | Coverage → E2E | T042–T049 | Coverage validation + E2E scenarios + persistence/performance checks |