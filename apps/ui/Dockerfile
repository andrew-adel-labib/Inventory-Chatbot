FROM python:3.11-slim

WORKDIR /app

ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]