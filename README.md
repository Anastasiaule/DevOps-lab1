# Library CI/CD

Учебный Flask-проект для лабораторной работы по методологии CI/CD.

## Стек
- Python
- Flask
- SQLite
- pytest
- Jenkins

## Сущности
- Books
- Authors
- Genres
- Publishers

Для каждой сущности реализованы 5 операций:
- POST — Create
- GET — List
- GET /id — Read
- PUT /id — Update
- DELETE /id — Delete

Всего: 20 операций.

## Запуск

```bash
py -m venv .venv
.venv\Scripts\activate
py -m pip install -r requirements.txt
py -m pytest -v
py run.py
```

Приложение будет доступно на http://127.0.0.1:5000

## Jenkins

Pipeline описан в `Jenkinsfile`.
Он получает код из GitHub, устанавливает зависимости и запускает pytest.
