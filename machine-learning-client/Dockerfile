# Use lightweight Python image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipenv files first to install deps early
COPY Pipfile Pipfile.lock ./

# Install dependencies from Pipenv
RUN pipenv install --deploy --ignore-pipfile

# Copy the rest of your application
COPY . .

# Run the ML client
CMD ["pipenv", "run", "python", "ml.py"]
