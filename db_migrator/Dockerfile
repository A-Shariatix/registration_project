FROM python:3.11.6
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY db_migrator.py .
ENTRYPOINT ["python3", "-u", "db_migrator.py"]
