FROM python:3.10-alpine

WORKDIR /demo-app

RUN pip install --no-cache-dir fastapi uvicorn

COPY . .

ENV PYTHONUNBUFFERED=1

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0" ]

CMD [ "--port", "8000" ]