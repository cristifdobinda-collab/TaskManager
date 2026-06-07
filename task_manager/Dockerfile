FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p instance \
    && useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

ENV FLASK_APP=run.py \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

CMD ["python", "run.py"]
