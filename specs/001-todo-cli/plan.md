# Implementation Plan: Todo CLI 기본 기능

**Branch**: `001-cli-todo-app` | **Date**: 2026-05-03 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-todo-cli/spec.md`

## Summary

이 구현 계획은 터미널 기반 Todo 관리 CLI 앱을 Python 3.12로 작성하는 방법을 정의합니다. 핵심 비즈니스 로직은 `todo_lib/` 패키지에 두고, `cli/` 레이어는 `typer`를 사용해 명령 입력을 파싱하며 `todo_lib` 호출만 담당합니다. 데이터 저장은 SQLite 로컬 파일(`todo.db`)이며, 테스트는 `pytest`와 `pytest-cov`로 작성합니다.

## Technical Context

**Language/Version**: Python 3.12
**Primary Dependencies**: typer, sqlalchemy
**Storage**: SQLite 로컬 파일 기반 저장소
**Testing**: pytest, pytest-cov
**Target Platform**: 터미널 실행 환경, 로컬 데스크톱/노트북
**Project Type**: CLI 도구
**Performance Goals**: 로컬 커맨드 응답 시간 200ms 이하, 단일 명령 실행 시 사용자 체감 지연 최소화
**Constraints**: REST API/GUI 없음, 추가 외부 패키지 불허, 추상 인터페이스 사용 금지, 단순 함수/클래스 중심 구현
**Scale/Scope**: 개인 개발자가 사용할 단일 사용자 로컬 Todo 관리, 수백 개 항목까지 지원

## Constitution Check

- 레이어 분리: `todo_lib/`는 비즈니스 로직과 DB 처리를 담당하고, `cli/`는 오직 입력 파싱과 `todo_lib` 호출만 수행합니다.
- 테스트 우선: 테스트 파일을 먼저 설계하고, 구현은 해당 테스트를 만족하도록 작성합니다.
- 최소 의존성: 런타임 의존성은 `typer`, `sqlalchemy`에 한정하며 추가 패키지 도입을 금지합니다.
- 단순함 우선: `ITodoRepository` 같은 추상 인터페이스를 쓰지 않고, 클래스와 함수 중심으로 직접 구현합니다.
- CLI 도구: `todo add`, `todo list`, `todo done`, `todo delete` 명령을 통해 터미널 전용 도구로 설계합니다.

## Project Structure

```text
todo_lib/
├── __init__.py
├── models.py        # SQLAlchemy ORM 모델 정의
├── db.py            # SQLite 엔진, 세션, 테이블 초기화
└── operations.py    # add/list/done/delete 비즈니스 로직

cli/
├── __init__.py
└── main.py          # Typer CLI 앱 정의, todo_lib 호출

tests/
├── conftest.py      # 테스트 DB 및 공통 fixtures
├── test_add.py      # todo 추가 테스트
├── test_list.py     # 목록 조회 및 필터링 테스트
└── test_update_delete.py # 완료 처리 및 삭제 테스트

contracts/
└── cli-contract.md  # CLI 명령 인터페이스 계약

pyproject.toml        # uv 패키지 관리, deps 및 스크립트 설정
uv.lock               # uv 잠금 파일
README.md             # 설치, 사용법 및 테스트 문서
```

**Structure Decision**: 단일 CLI 애플리케이션 구조를 선택합니다. `todo_lib/`는 비즈니스 로직과 데이터 계층을 캡슐화하고, `cli/`는 사용자 명령을 해석하여 `todo_lib`에 위임합니다. 이 방식은 constitution의 레이어 분리와 단순함 원칙을 모두 만족합니다.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 없음 | | |
