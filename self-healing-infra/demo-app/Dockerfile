FROM python:3.10-alpine

WORKDIR /demo-app

RUN apk add --no-cache gcc musl-dev linux-headers \
    && pip install --no-cache-dir fastapi uvicorn psutil opentelemetry-api opentelemetry-sdk opentelemetry-exporter-otlp \
    && apk del gcc musl-dev linux-headers

COPY . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "uvicorn", "app:app", "--host", "0.0.0.0" ]

CMD [ "--port", "8000" ]