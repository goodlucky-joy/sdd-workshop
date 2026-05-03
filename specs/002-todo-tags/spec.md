# Feature Specification: Todo tags

**Feature Branch**: `002-todo-tags`  
**Created**: 2026-05-03  
**Status**: Draft  
**Input**: User description: "기존 Todo 앱에 태그 기능을 추가하고 싶어.

추가할 기능:
1. Todo 항목 생성 시 태그를 선택적으로 추가할 수 있다
    - 태그는 최대 5개까지 허용
    - 각 태그는 20자 이내
    - 태그 없이도 Todo 생성 가능 (기존 기능 유지)
2. 목록 조회 시 태그로 필터링할 수 있다
    - todo list --tag 태그명 형식

이슈 번호: #1, #2
기존 Todo 기능(추가/조회/완료/삭제)은 그대로 유지되어야 해."

## User Scenarios & Testing *(mandatory)*



### User Story 1 - Create a Todo with optional tags (Priority: P1)

A user can create a new Todo item and optionally attach zero to five tags while keeping the existing Todo flow.

**Why this priority**: This is the core behavior of the feature; without it, tags cannot be used at all.

**Independent Test**: Add Todos with and without tags, then verify the Todo list shows the new items and tag values correctly.

**Acceptance Scenarios**:

1. **Given** the user creates a Todo with one to five valid tags, **When** they submit the add command, **Then** the Todo is created and stores each provided tag.
2. **Given** the user creates a Todo without tags, **When** they submit the add command, **Then** the Todo is created successfully with no tags attached.
3. **Given** the user includes a tag longer than 20 characters, **When** they submit the add command, **Then** the system rejects the Todo creation and returns a validation error.
4. **Given** the user includes duplicate tag values in one Todo creation request, **When** they submit the add command, **Then** the system rejects the request and reports duplicate tags.

---

### User Story 2 - Filter Todo list by tag (Priority: P2)

A user can view only Todo items containing a specific tag using the tag filter option.

**Why this priority**: Tag filtering demonstrates the value of tags and supports users who need to focus on tagged work.

**Independent Test**: Create several Todos with varying tags and verify that `todo list --tag <tag>` returns only matching items.

**Acceptance Scenarios**:

1. **Given** multiple Todos exist with different tags, **When** the user runs `todo list --tag 업무`, **Then** only Todos containing the tag `업무` are shown.
2. **Given** no Todo contains the requested tag, **When** the user runs `todo list --tag unknown`, **Then** the result is either an empty list or a clear message that no matching Todos were found.
3. **Given** Todos contain the same tag with different casing, **When** the user filters by that tag, **Then** matching is case-insensitive and all relevant Todos are included.

---

### User Story 3 - Preserve existing Todo behavior (Priority: P3)

A user can continue to use the existing add, list, complete, and delete commands without specifying tags.

**Why this priority**: The new feature must not break the existing Todo app for users who do not use tags.

**Independent Test**: Run the existing command flows without tag options and verify the behavior is unchanged.

**Acceptance Scenarios**:

1. **Given** a user adds a Todo with no tag options, **When** they submit the add command, **Then** the Todo is created exactly as before.
2. **Given** a user lists Todos without `--tag`, **When** they run the list command, **Then** all eligible Todos are shown regardless of tags.
3. **Given** a user marks a Todo complete or deletes it, **When** they perform the action, **Then** the completion and deletion flows work the same as before.

---

### Edge Cases

- If the user submits more than five tags during creation, the request is rejected with a validation error explaining the 5-tag limit.
- If a tag contains more than 20 characters, the request is rejected with a validation error explaining the 20-character limit.
- If duplicate tags appear in the same creation request, the request is rejected with a duplicate-tag validation error.
- If the user filters by a tag that does not exist on any Todo, the list command returns no items and communicates the empty result clearly.
- If the user creates Todos with tags and later lists without `--tag`, all Todos are shown, including those with and without tags.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow a Todo item to be created with zero to five tags.
- **FR-002**: System MUST validate that each tag is no longer than 20 characters.
- **FR-003**: System MUST reject Todo creation when the same tag appears more than once in the same request.
- **FR-004**: System MUST allow users to list Todos filtered by a single tag using `todo list --tag <tag>`.
- **FR-005**: System MUST ensure tag filtering returns only Todos containing the requested tag.
- **FR-006**: System MUST preserve existing Todo creation, listing, completion, and deletion behavior when tags are not provided.
- **FR-007**: System MUST handle unknown tag filters by returning no matching Todos and not failing unexpectedly.
- **FR-008**: System MUST treat tag matching as case-insensitive for filter lookup.
- **FR-009**: System MUST display tag values in Todo list output when a Todo has tags.

### CLI Interface

#### Tag Input Format
- Tags are provided using the `--tag` option, which can be repeated up to 5 times.
- Example: `todo add "회의 준비" --tag 업무 --tag 중요 --tag 긴급`
- Tags without `--tag` prefix are not accepted.
- Tag values are trimmed of leading/trailing whitespace.

#### Output Format
- Todo list displays tags in square brackets before the title.
- Example: `[업무, 중요] 회의 준비`
- Todos without tags display normally without brackets.
- Example: `보고서 작성`

#### Filter Combination Rules
- `--tag` can be combined with existing filters like `--filter` or `--priority`.
- All filters must match for a Todo to be included (AND logic).
- Example: `todo list --tag 업무 --filter pending` shows only pending Todos with the "업무" tag.
- If conflicting filters are provided, the command fails with a clear error message.



### Key Entities *(include if feature involves data)*

- **Todo**: A task item with an optional set of tags. Key attributes include title, completion state, and tags.
- **Tag**: A text label attached to a Todo. Key attributes include the tag text and its association with one or more Todo items.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a Todo with zero to five tags and confirm the tags appear in the Todo listing.
- **SC-002**: `todo list --tag <tag>` returns only Todos containing that tag and excludes non-matching Todos.
- **SC-003**: Existing Todo add, list, complete, and delete commands continue to work without tag options.
- **SC-004**: The system rejects tags longer than 20 characters and duplicate tags in a single Todo creation request.
- **SC-005**: Tag filtering is case-insensitive and returns the same results regardless of input casing.

## Assumptions

- Tag entry is optional; users may create Todos with no tags and preserve existing behavior.
- Tag values are normalized for comparison but the original casing may be stored or displayed consistently.
- Only a single `--tag <tag>` filter is required for this feature; multiple tag filters are out of scope for this iteration.
- Editing or removing tags after Todo creation is out of scope for this feature.
- Existing Todo fields and commands remain unchanged unless required to support tag display or filtering.
