# Weather App

App to fetch some weather data from https://openweathermap.org/
## Download:

```
gitclone
```
## Run with Python

You need python 3.8 or greater
```
pip3 install pipenv
pipenv run weatherapp forecast Santander,ES --units=metric --days=3
```
## Run with Docker-Compose
```
docker-compose build && docker-compose up -d && docker-compose exec weatherapp sh
```
Then you can run:
```
pipenv run weatherapp current Madrid,ES
```

## Usage
```
pipenv run weatherapp -h
```