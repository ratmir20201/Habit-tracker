FROM python:3.12

ENV PYTHONUNBUFFERED=1

WORKDIR /bot

COPY bot/pyproject.toml bot/poetry.lock ./

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY bot /bot

CMD ["python", "main.py"]
