# Research: Todo CLI 기본 기능

## Decision

- Python 3.12을 사용합니다.
- CLI 프레임워크로 `typer`를 사용합니다.
- 데이터 저장은 SQLite 로컬 파일로 구현합니다.
- ORM으로 `sqlalchemy`를 사용하지만, 과도한 추상화 없이 직접 모델과 세션을 관리합니다.
- 테스트는 `pytest`와 `pytest-cov`로 작성합니다.

## Rationale

- Python 3.12는 최신 Python 기능을 활용할 수 있으면서 교육용 CLI 도구 구현에 적합합니다.
- `typer`는 명령어 정의가 간결하고, CLI 스크립트에서 사용자 입력 파싱을 쉽고 명확하게 처리합니다.
- SQLite는 로컬 파일 기반 저장소로 설치와 운영이 간편하며, 서버가 필요하지 않습니다.
- `sqlalchemy`를 ORM으로 사용하면 데이터 모델과 CRUD 동작을 명확하게 구현할 수 있습니다.
- `pytest`는 Python 테스트 생태계에서 표준이며, `pytest-cov`는 커버리지 측정을 통해 테스트 우선 원칙을 보장합니다.

## Alternatives Considered

- `click` 대신 `typer`: `typer`는 타입 힌트를 활용하여 CLI 명세를 더 명확하게 만들 수 있어 선택했습니다.
- 파일 기반 JSON 저장소 대신 SQLite: SQLite는 SQLAlchemy와 자연스럽게 연계되며, 추후 데이터 모델 확장에도 유리합니다.
- 추가 패키지 도입 없음: constitution의 최소 의존성 원칙에 따라 `typer`, `sqlalchemy`, `pytest`, `pytest-cov` 외 라이브러리를 추가하지 않습니다.
