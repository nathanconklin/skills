FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/scripts \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

WORKDIR /app

COPY requirements.txt /app/requirements.txt
COPY service/requirements.txt /app/service/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt -r /app/service/requirements.txt \
    && python -m playwright install --with-deps chromium

COPY scripts /app/scripts
COPY service /app/service

RUN useradd --create-home --uid 10001 exporter \
    && mkdir -p /tmp/shared-url-to-markdown-service \
    && chown -R exporter:exporter /tmp/shared-url-to-markdown-service

USER exporter
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
    CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).read()"]

CMD ["uvicorn", "service.app:app", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
