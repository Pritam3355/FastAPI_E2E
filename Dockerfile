FROM python:3.11-slim

WORKDIR /code

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

COPY ./app /code/app
COPY ./alembic /code/alembic
COPY alembic.ini /code/alembic.ini

# DATABASE_URL will come from docker-compose environment
# Add debug commands
CMD echo "Running Alembic migrations..." && \
    alembic upgrade head && \
    echo "Migrations complete. Starting server..." && \
    uvicorn app.main:app --host 0.0.0.0 --port 8000