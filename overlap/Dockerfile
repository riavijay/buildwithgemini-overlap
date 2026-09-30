FROM python:3.11-slim

WORKDIR /app

# Prevent python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run FastAPI app with uvicorn listening on port 8080
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
