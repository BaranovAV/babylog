FROM python:3.10-slim-bookworm AS requirements-builder

WORKDIR /

COPY poetry.lock pyproject.toml ./

RUN pip install poetry==$(head -n1 poetry.lock | awk -F' ' '{ print $9 }')

RUN poetry export --format=requirements.txt > requirements.txt


FROM python:3.10-slim-bookworm AS app

WORKDIR /app

RUN apt update && apt install -y gcc && pip install -U pip && pip install uwsgi

COPY --from=requirements-builder /requirements.txt ./

RUN pip install -r requirements.txt

COPY src ./

CMD uwsgi --http :8000 --module core.wsgi
