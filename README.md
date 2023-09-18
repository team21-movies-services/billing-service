# billing-service

* link = https://github.com/team21-movies-services/billing-service

# Стек технологий
- Frontend (Nginx) - маршрутизация запросов
- Backend (Fastapi) - получение и обработка запросов пользователя

## backend библиотеки
* `fastapi` - основной backend фреймворк
* `pydantic` - валидация входящих данных api
* `uvicorn` - локальный запуск проекта, `gunicorn` - запуск в прод. окружении
* `pyjwt` - библиотека для работы с jwt


### Линтеры
* flake8, mypy, bandit

# Init development

1) init poetry and pre-commit
```bash
poetry install --no-root
```

```bash
poetry run pre-commit install
```

2) env
```bash
cp ./.env.template ./.env
```

```bash
cp ./src/.env.template ./src/.env
```

3) build and up docker local
```bash
make build-local
make up-local
```

4) go to `http://localhost:8000/docs`
