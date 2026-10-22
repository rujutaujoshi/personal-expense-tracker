
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

COPY app.py database.py ./

COPY templates/ ./templates/
COPY static/ ./static/

RUN mkdir -p /app/data

ENV PYTHONUNBUFFERED=1
ENV DATABASE_PATH=/app/data/expenses.db

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
