FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN useradd -m appuser
USER appuser

COPY src /app

EXPOSE 8000

HEALTHCHECK CMD python -c "print('ok')" || exit 1

CMD ["python", "main.py"]