# Use lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipenv files first to install deps early
COPY Pipfile ./

# Install dependencies from Pipenv
RUN pipenv install --deploy --ignore-pipfile

# Install pydub dependencies
RUN apt-get update && apt-get install -y ffmpeg flac

# Copy the rest of your application
COPY . .

# Expose port for Flask app
EXPOSE 5002

# Run the ML client
CMD ["pipenv", "run", "python", "ml_server.py"]
