FROM python:3.11-slim

WORKDIR /service-a

# Upgrade pip and install packages without caching
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn

COPY main.py .

EXPOSE 5000

ENTRYPOINT [ "uvicorn", "main:app", "--host", "0.0.0.0" ]

CMD [ "--port", "5000" ]