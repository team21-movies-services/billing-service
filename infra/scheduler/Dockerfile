FROM python:3.11-slim

ENV SRC_DIR=/opt


ENV APP_USER=scheduler-user

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

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
RUN poetry install --no-root --only scheduler

# Копирования кода приложения
COPY ./src/worker $SRC_DIR/worker
COPY ./src/shared $SRC_DIR/shared

COPY infra/backend/entrypoint.sh /usr/local/bin/entrypoint.sh
