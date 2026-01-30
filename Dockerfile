FROM python:3.11-slim

WORKDIR /app

RUN mkdir -p /app/logs

RUN apt-get update \
  && apt-get install -y --no-install-recommends git ca-certificates \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install --no-cache-dir -e .

ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "awardsreport.main:app", "--host", "0.0.0.0", "--port", "8000"]