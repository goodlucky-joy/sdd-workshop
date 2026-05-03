# CLI Contract: Todo CLI 기본 기능

## CLI 명령 인터페이스

### `todo add "<제목>" [--due YYYY-MM-DD] [--priority high|medium|low]`
- 동작: 새로운 Todo 항목을 추가한다.
- 필수: 제목
- 선택: 마감일(`YYYY-MM-DD`), 우선순위(`high`, `medium`, `low`)
- 오류:
  - 제목이 비어있으면 `❌ Title is required` 메시지 출력
  - 날짜 형식이 잘못되면 `❌ Invalid date format` 메시지 출력

### `todo list [--filter done|pending] [--priority high|medium|low]`
- 동작: Todo 목록을 조회한다.
- 옵션:
  - `--filter done` 완료된 항목만 표시
  - `--filter pending` 미완료 항목만 표시
  - `--priority`로 우선순위 필터링
- 기본 동작: 필터 없이 모든 항목을 표시

### `todo done <id>`
- 동작: 지정된 ID Todo 항목을 완료 상태로 표시한다.
- 오류:
  - 존재하지 않는 ID를 입력하면 `❌ Todo item not found` 메시지 출력

### `todo delete <id>`
- 동작: 지정된 ID Todo 항목을 삭제한다.
- 오류:
  - 존재하지 않는 ID를 입력하면 `❌ Todo item not found` 메시지 출력
