# STAGE 1: Builder
FROM python:3.14-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y gcc

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


# STAGE 2: Runner
FROM python:3.14-slim

WORKDIR /app

RUN adduser --disabled-password --gecos "" --uid 5678 appuser

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

COPY . .
RUN chown -R appuser:appuser /app

USER appuser
ENV FLASK_APP=run.py
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]