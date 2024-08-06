ARG PYTHON_VERSION=3.10
ARG EXTERNAL_PORT=8000
FROM python:${PYTHON_VERSION}-slim
ARG CACHEBUST=1

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE ${EXTERNAL_PORT}

CMD ["sh", "-c", "uvicorn app.main:app --reload --host 0.0.0.0 --port $EXTERNAL_PORT"]

