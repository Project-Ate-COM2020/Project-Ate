FROM python:3.14.3-slim
WORKDIR /backend/
LABEL authors="jacob"
COPY requirements.txt .env ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["gunicorn", "backend.wsgi", "--bind", "0.0.0.0:8000"]
