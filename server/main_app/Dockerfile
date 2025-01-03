FROM python:3.11-slim
WORKDIR /app

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# CMD ["uvicorn", "http_app:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["hypercorn", "http_app:app", "--bind", "0.0.0.0:8000"]
