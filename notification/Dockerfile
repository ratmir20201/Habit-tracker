FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /notification

COPY notification/pyproject.toml notification/poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY notification /notification

CMD ["python", "main.py"]
