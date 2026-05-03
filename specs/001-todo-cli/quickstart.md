# Quickstart: Todo CLI 기본 기능

## 설치

1. `uv`를 사용하여 프로젝트를 설치합니다.

```powershell
uv install typer sqlalchemy pytest pytest-cov
```

2. 개발 환경을 준비합니다.

```powershell
uv install --dev pytest pytest-cov
```

## 실행

`todo` CLI를 실행하려면 `cli/main.py`를 직접 호출합니다.

```powershell
python -m cli.main add "Buy groceries" --due 2026-05-10 --priority high
python -m cli.main list
python -m cli.main done 1
python -m cli.main delete 1
```

## 주요 명령어

- `todo add "<제목>" [--due YYYY-MM-DD] [--priority high|medium|low]`
- `todo list [--filter done|pending] [--priority high|medium|low]`
- `todo done <id>`
- `todo delete <id>`

## 테스트

```powershell
pytest --cov=todo_lib
```

## 데이터 저장

- Todo 데이터는 로컬 `todo.db` SQLite 파일에 저장됩니다.
- 서버나 네트워크 연결이 필요하지 않습니다.
