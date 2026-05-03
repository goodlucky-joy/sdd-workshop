# Tasks: Todo CLI 기본 기능

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: `plan.md`, `spec.md`

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

**Purpose**: 비즈니스 로직과 데이터 계층을 구축하여 모든 스토리 작업의 기반을 준비한다.

- [ ] T008 Create `todo_lib/models.py` and define `Todo` ORM model with `id`, `title`, `due_date`, `priority`, `done`, `created_at`
- [ ] T009 Create `todo_lib/db.py` and implement SQLite engine creation, session management, and `create_tables()` helper
- [ ] T010 Create `todo_lib/operations.py` and add operation stubs for `add_todo()`, `list_todos()`, `mark_todo_done()`, `delete_todo()`
- [ ] T011 Create `tests/conftest.py` with fixtures for an isolated SQLite test database and session factory
- [ ] T012 Create `cli/main.py` command wiring to call `todo_lib.operations` stubs for each command

---

## Phase 3: User Story 1 - Todo 추가 및 기본 항목 생성 (Priority: P1) 🎯 MVP

**Goal**: `todo add` 명령으로 제목 필수, 선택적 마감일과 우선순위를 가진 Todo 항목을 추가할 수 있다.

**Independent Test**: `todo add` 명령을 실행하여 새 항목이 생성되고 목록에 반영되는지 확인한다.

### Tests for User Story 1

- [ ] T013 [P] [US1] Create `tests/test_add.py` with pytest cases for valid add, due date/priority persistence, and title-required validation

### Implementation for User Story 1

- [ ] T014 [US1] Implement `add_todo()` in `todo_lib/operations.py` with title validation, optional `due_date` parsing on `YYYY-MM-DD`, and `priority` values `High|Medium|Low`
- [ ] T015 [US1] Implement `todo add` command in `cli/main.py` to parse `--due` and `--priority` and call `todo_lib.operations.add_todo()`
- [ ] T016 [US1] Update `README.md` with `todo add` usage examples and validation rules

---

## Phase 4: User Story 2 - Todo 목록 조회 및 필터링 (Priority: P1)

**Goal**: `todo list` 명령으로 전체 목록 조회와 완료 상태 및 우선순위 필터링이 가능하다.

**Independent Test**: 몇 개의 Todo를 추가한 뒤 `todo list` 명령으로 필터 결과가 정확한지 확인한다.

### Tests for User Story 2

- [ ] T017 [P] [US2] Create `tests/test_list.py` with pytest cases for default list, `--filter done|pending`, and `--priority high|medium|low`

### Implementation for User Story 2

- [ ] T018 [US2] Implement `list_todos()` in `todo_lib/operations.py` to support filtering by `done` status and priority
- [ ] T019 [US2] Implement `todo list` command in `cli/main.py` with `--filter` and `--priority` options
- [ ] T020 [US2] Update `README.md` with `todo list` command examples and filter usage

---

## Phase 5: User Story 3 - Todo 완료 처리 (Priority: P2)

**Goal**: `todo done <id>` 명령으로 항목을 완료 상태로 표시할 수 있다.

**Independent Test**: 완료되지 않은 항목에 `todo done <id>`를 실행하여 완료 상태로 변경되는지 확인한다.

### Tests for User Story 3

- [ ] T021 [P] [US3] Extend `tests/test_update_delete.py` with pytest cases for `todo done <id>` success and invalid ID error handling

### Implementation for User Story 3

- [ ] T022 [US3] Implement `mark_todo_done()` in `todo_lib/operations.py` to mark an item complete by ID and raise if not found
- [ ] T023 [US3] Implement `todo done` command in `cli/main.py` to call `mark_todo_done()` and display success or error messages
- [ ] T024 [US3] Update `README.md` with `todo done` command usage and expected output

---

## Phase 6: User Story 4 - Todo 삭제 (Priority: P2)

**Goal**: `todo delete <id>` 명령으로 항목을 삭제할 수 있다.

**Independent Test**: `todo delete <id>`를 실행하여 항목이 목록에서 제거되는지 확인한다.

### Tests for User Story 4

- [ ] T025 [P] [US4] Extend `tests/test_update_delete.py` with pytest cases for `todo delete <id>` success and invalid ID error handling

### Implementation for User Story 4

- [ ] T026 [US4] Implement `delete_todo()` in `todo_lib/operations.py` to delete a Todo by ID and raise if not found
- [ ] T027 [US4] Implement `todo delete` command in `cli/main.py` to call `delete_todo()` and display success or error messages
- [ ] T028 [US4] Update `README.md` with `todo delete` command usage and expected output

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: 전체 구현을 정리하고 테스트/문서를 완성한다.

- [ ] T029 [P] Run `pytest` with `pytest-cov` and fix any failing tests
- [ ] T030 [P] Ensure `README.md` describes installation, command usage, and validation rules clearly
- [ ] T031 [P] Verify `todo_lib/db.py` creates `todo.db` in the local working directory and does not require a server

---

## Dependencies & Execution Order

- **Phase 1** must complete before most implementation begins.
- **Phase 2** must complete before any story-specific implementation.
- **Phase 3** and **Phase 4** are both P1 stories and may be developed in parallel after Phase 2.
- **Phase 5** and **Phase 6** are P2 stories and may follow after Phase 2, but can also be worked in parallel with each other.
- **Phase 7** depends on completion of all preceding story phases.

### User Story Dependencies

- **US1**: No internal story dependency once foundational pieces exist.
- **US2**: No internal story dependency once foundational pieces exist.
- **US3**: No internal story dependency once foundational pieces exist.
- **US4**: No internal story dependency once foundational pieces exist.

### Parallel Opportunities

- `T005`, `T006`, and `T011` can run in parallel because they touch distinct files.
- `T013`, `T017`, `T021`, and `T025` can run in parallel as independent test creation tasks.
- `T014` and `T018` can run in parallel after their respective tests are written.
- Final polish tasks `T029`–`T031` can run after all story implementations are complete.
