# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install pipenv
RUN pip install pipenv

# Copy Pipenv files first to install deps early
COPY Pipfile Pipfile.lock ./

# Install dependencies
RUN pipenv install --deploy --ignore-pipfile

# Copy rest of the app (code, static files, templates)
COPY . .

# Expose port for Flask app
EXPOSE 5001

# Run the Flask app
CMD ["pipenv", "run", "python", "app.py"]
