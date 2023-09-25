FROM python:3.11

WORKDIR /app
COPY pyproject.toml poetry.lock ./

EXPOSE 3000

ENV \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1
ENV \
    POETRY_VERSION=$POETRY_VERSION \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1

RUN pip3 install poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi

COPY .. .

CMD ["alembic", "upgrade", "head"]

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000", "--reload"]