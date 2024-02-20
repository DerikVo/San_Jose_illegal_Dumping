FROM python:3.9

RUN pip install pandas requests sqlalchemy psycopg2

WORKDIR /app

COPY api_pull.py api_pull.py

ENTRYPOINT ["python", "api_pull.py"]

