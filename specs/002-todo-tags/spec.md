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

A user can create a new Todo item and optionally attach up to five tags while keeping the existing Todo creation flow.

**Why this priority**: This adds the core tagging capability and must work first because it enables all downstream tag-based behaviors.

**Independent Test**: Create a Todo with and without tags; verify the item is saved and displayed with the expected tag list.

**Acceptance Scenarios**:

1. **Given** the user is creating a Todo, **When** they provide one to five valid tags, **Then** the Todo is created with those tags attached.
2. **Given** the user is creating a Todo, **When** they create it without tags, **Then** the Todo is created successfully and no tags are attached.
3. **Given** the user submits a tag longer than 20 characters, **When** the item is created, **Then** the request is rejected with a validation error and the Todo is not created.
4. **Given** the user submits duplicate tags in the same Todo, **When** the item is created, **Then** the request is rejected with a validation error about duplicate tags.

---

### User Story 2 - Filter Todo list by tag (Priority: P2)

A user can view only Todo items that contain a specific tag using the tag filter command.

**Why this priority**: Tag filtering is the primary means for users to find tagged items and validates the usefulness of tags.

**Independent Test**: Create several Todos with different tags and run the list command with a tag filter to confirm only matching items appear.

**Acceptance Scenarios**:

1. **Given** multiple Todos exist with different tags, **When** the user runs `todo list --tag 업무`, **Then** only Todos containing the tag `업무` are displayed.
2. **Given** no Todo contains the requested tag, **When** the user runs `todo list --tag unknown`, **Then** the result is an empty list or a clear message stating no matching Todos were found.
3. **Given** Todo items have the same tag with different letter casing, **When** the user filters by that tag, **Then** matching is case-insensitive and all relevant items are included.

---

### User Story 3 - Preserve existing Todo behavior (Priority: P3)

A user can continue to add, list, complete, and delete Todos without using tags, and existing commands behave as before.

**Why this priority**: The feature must not break the current Todo app experience for users who are not using tags.

**Independent Test**: Run the existing add, list, done, and delete flows with no tag arguments and confirm they work unchanged.

**Acceptance Scenarios**:

1. **Given** a user adds a Todo without tag options, **When** the item is created, **Then** it behaves exactly like existing Todo creation.
2. **Given** a user lists all Todos without `--tag`, **When** they view the list, **Then** all eligible Todos are displayed regardless of tags.
3. **Given** a user marks a Todo complete or deletes it, **When** they perform the action, **Then** the completion and deletion flows work the same as before.

---

### Edge Cases

- What happens when the user submits more than five tags during Todo creation?
- What happens when a tag contains more than 20 characters?
- What happens when the same tag is provided more than once in the same Todo creation request?
- What happens if the user filters by a tag that does not exist on any Todo?
- What happens if the user creates a Todo with tags and later uses the existing list command without a filter?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create a Todo item with zero to five tags.
- **FR-002**: System MUST validate that each tag is no longer than 20 characters.
- **FR-003**: System MUST reject creation of a Todo if the same tag appears more than once in the same request.
- **FR-004**: System MUST allow users to list Todos filtered by a single tag using `todo list --tag <tag>`.
- **FR-005**: System MUST ensure that filtering by tag returns only Todos containing that exact tag.
- **FR-006**: System MUST continue to support existing Todo creation, listing, completion, and deletion behavior when no tags are provided.
- **FR-007**: System MUST handle requests for unknown tags by returning no matching Todos and not failing unexpectedly.

### Key Entities *(include if feature involves data)*

- **Todo**: A task item with an optional set of tags. Key attributes include title, completion state, and a list of attached tags.
- **Tag**: A text label attached to a Todo. Key attributes include a string value and a relationship to one or more Todo items.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a Todo with zero to five tags in a single action and see the assigned tags reflected in the Todo listing.
- **SC-002**: Tag filtering returns only Todos that contain the requested tag and excludes Todos without that tag.
- **SC-003**: Existing Todo add, list, complete, and delete commands continue to work when tags are not used.
- **SC-004**: Validation rejects tags longer than 20 characters and duplicate tags during Todo creation, with a clear user-facing message.

## Assumptions

- Tag entry is optional; users may create Todos with no tags and preserve the existing behavior.
- Tag values are treated case-insensitively for filtering and matching.
- Only a single `--tag <tag>` filter is required for this feature; multi-tag filtering is out of scope.
- Editing or removing tags after Todo creation is out of scope for this initial feature.
