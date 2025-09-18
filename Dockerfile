# Python Image
FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    git \
    libpq-dev \
    postgresql \
    postgresql-client \
    postgresql-contrib \
    build-essential \
    python3-dev \
    libc6-dev \
    gcc \
    sudo \
    && rm -rf /var/lib/apt/lists/* \

WORKDIR /app
ENV PYTHONPATH /app


COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

RUN chmod +x start.sh
ENTRYPOINT ["/start.sh"]
# command: gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 src.main:app
