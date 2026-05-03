# Todo CLI

터미널 기반 Todo 관리 도구입니다.

## 설치

```bash
python -m pip install .
python -m pip install -e .[dev]
```

## 사용법

```bash
todo add "Buy milk" --due 2026-12-31 --priority High
todo list
todo list --filter pending
todo done 1
todo delete 1
```

## 테스트

```bash
pytest
```
