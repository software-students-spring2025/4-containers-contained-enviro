FROM python:3.11-slim

WORKDIR /app

COPY seed_movies.py .
COPY movies.csv .

RUN pip install pymongo python-dotenv

CMD ["python", "seed_movies.py"]