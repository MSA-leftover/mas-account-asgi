## global
ARG WORKDIR="/opt/msa-account-asgi"

## builder
FROM python:3.10 AS builder

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN pip install poetry && poetry config virtualenvs.in-project true

ARG WORKDIR
WORKDIR ${WORKDIR}
COPY ./src ./

RUN poetry install --only main

## runner
FROM python:3.10-apline

ARG WORKDIR
WORKDIR ${WORKDIR}

COPY --from=builder ${WORKDIR} .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
