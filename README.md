# Weather App

App to fetch some weather data from https://openweathermap.org/
## Download:

```
git clone https://github.com/kaliwey/weatherapp.git
```

## Configuration:

Set APIKEY in .env file

You can obtain apikey registering on https://openweathermap.org/
```
APIKEY=xxxxxxxxxx
```
## Run with Python

You need python 3.8 (or greater) and pip3 installed
```
pipenv install
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