FROM python:3.11-slim as main

# Основной путь приложения
ENV SRC_DIR=/opt

# Путь до приложения fastapi
ENV APP_DIR=$SRC_DIR/app
ENV SHARED_DIR=$SRC_DIR/shared

ENV APP_USER=backend-user

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    GUNICORN_PROCESSES=4 \
    GUNICORN_CONNECTIONS=8 \
    GUNICORN_LOGLEVEL='error'

# Создание no-root пользователя
RUN groupadd -r $APP_USER && \
    useradd -d $SRC_DIR -r -g $APP_USER $APP_USER && \
    chown $APP_USER:$APP_USER -R $SRC_DIR

USER $APP_USER

# Установка зависимостей
WORKDIR $SRC_DIR

ENV PATH="/$SRC_DIR/.local/bin:${PATH}"
RUN pip install --user --upgrade pip && \
    pip install --user --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
RUN poetry install --no-root --only main


# Копирования кода приложения
COPY ./src/app $APP_DIR
COPY ./src/shared $SHARED_DIR
COPY ./src/gunicorn.conf.py $APP_DIR

EXPOSE 8000

COPY infra/backend/entrypoint.sh /usr/local/bin/entrypoint.sh

FROM main as test

RUN poetry install --no-root

COPY ./src/tests $SRC_DIR/tests
COPY ./src/migrations $SRC_DIR/migrations
COPY ./src/alembic.ini $SRC_DIR/
COPY ./src/worker $SRC_DIR/worker