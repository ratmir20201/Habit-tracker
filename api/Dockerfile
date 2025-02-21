FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /api

COPY api/pyproject.toml api/poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY api /api

RUN apt-get update && apt-get install -y supervisor

COPY api/supervisord.ini /etc/supervisor/conf.d/supervisord.conf

# Запускаем supervisord, который выполнит миграции, запустит API и Kafka Producer
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
