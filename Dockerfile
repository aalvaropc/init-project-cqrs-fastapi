FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    postgresql-client \
    && apt-get clean

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
COPY wait_for_postgres.sh /usr/src/app/

RUN chmod +x /usr/src/app/wait_for_postgres.sh

EXPOSE 8000

CMD ["sh", "-c", "./wait_for_postgres.sh pg_primary && alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
