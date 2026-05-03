# Data Model: Todo CLI 기본 기능

## 엔티티

### Todo

- `id`: 정수, 기본 키, 자동 증가
- `title`: 문자열, 필수
- `due_date`: 날짜, 선택적, `YYYY-MM-DD` 형식으로 입력
- `priority`: 문자열, 선택적, `High`, `Medium`, `Low` 중 하나
- `done`: 불리언, 기본값 `False`
- `created_at`: 타임스탬프, 항목 생성 시 자동 설정

## Validation Rules

- 제목은 반드시 존재해야 한다. 비어 있는 제목은 허용되지 않는다.
- 마감일은 `YYYY-MM-DD` 형식이어야 한다.
- 우선순위는 `High`, `Medium`, `Low` 중 하나여야 하며, 지정하지 않으면 `None`으로 처리된다.

## 상태 전이

- 생성: 항목은 `done=False` 상태로 생성된다.
- 완료 처리: `todo done <id>` 명령 실행 시 `done=True`로 변경된다.
- 삭제: `todo delete <id>` 명령 실행 시 해당 항목이 데이터베이스에서 제거된다.

## 관계

- 단일 엔티티 모델만 사용합니다. 추가 엔티티나 조인 테이블은 필요하지 않습니다.
