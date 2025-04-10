![Lint-free](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/lint.yml/badge.svg)

![Event Logger](https://github.com/nyu-software-engineering/containerized-app-exercise/actions/workflows/event-logger.yml/badge.svg)

# Containerized App Exercise

Build a containerized app that uses machine learning. See [instructions](./instructions.md) for details.

## Team members
- [Lana Davydov](https://github.com/lanadavydov)
- [Jack Wang](https://github.com/JackInTheBox314)
- [Joylyn Gong](https://github.com/joylyngong)
- [Suhan Suresh](https://github.com/Suhansrh)

## Description

This web app provides a personalized experience for users to describe a movie that they are interested in viewing. Once they complete their voice recording, they will be provided with a film that most closely aligns with their interests based on the description that they spoke of.

## Instructions

### All services

To build and run all services:
1. `docker-compose up --build`
2. Visit `http://localhost:5001/`

To shut down: `docker-compose down -v`

### MongoDB

To build and run MongoDB:
```
docker run --name mongodb -d -p 27017:27017 \
  -v $(pwd)/mongo-init:/docker-entrypoint-initdb.d \
  mongo --auth
```

To open a MongoDB shell in the container and test it:
1. `docker exec -it mongodb mongosh`
2. `use ml_data`
3. `db.auth("ml_user", "ml_password")`
3. `show collections`

To shut down: `docker stop mongodb && docker rm mongodb`

### Web App

To build and run the Web App:
1. `cd web-app`
2. `docker build -t web-app .`
3. `docker run -p 5001:5001 --name web-app web-app`
4. Visit `http://localhost:5001/`

### Machine Learning Client

To build and run the Machine Learning Client:
1. `cd machine-learning-client`
2. `docker build -t ml-client .`
3. `docker run --name ml-client ml-client`

### Testing
## Running Unit Tests Locally

Running unit tests locally on the web app:
1. `cd web-app`
2. `pipenv install --dev`
3. `pipenv shell`
4. `pytest --cov=.`

Running unit tests locally on the ML Client:
1. `cd machine-learning-client`
2. `pipenv install --dev`
3. `pipenv shell`
4. `pytest --cov=.'
