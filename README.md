#  Example Pywren Flask REST API
Pywren Hello World REST API.

## Getting Started
Quickly set up an environment by running `pipenv install` and `pipenv install --dev`. The `--dev` flag will add linting, testing and an ipython terminal.

## Setting up Pywren
Either in a `.env` file add the following,

```
FLASK_APP='app.run'
FLASK_ENV='development'
PYWREN_STORAGE_BUCKET=<BUCKET_NAME>
PYWREN_IBM_CF_ENDPOINT=<HOST>
PYWREN_IBM_CF_NAMESPACE=<NAMESPACE>
PYWREN_IBM_CF_API_KEY=<API_KEY>
PYWREN_IBM_COS_ENDPOINT=<REGION_ENDPOINT>
PYWREN_IBM_COS_API_KEY=<API_KEY>
```

for more information see the [official docs](https://github.com/pywren/pywren-ibm-cloud#using-configuration-file)

## Running
Once you've set you pywren config variables, you can activate your environment with `pipenv shell`, and run the application with `flask run`. 

You can then naviagte to the home route `http://localhost:5000` which will redirect you to `http://localhost:5000/api/v1/`

## Getting data with requests.
Once the application is up and running you can sent a POST request with requests in a separate terminal.

```
import requests
r = requests.post("http://localhost:5000/api/v1/pywren-hello-world", json={'iterdata': [1,2,3,4]})
data = r.json()
print(data)
>>> {'result': 38}
```


## Install Redis docker image
These are the instructions for installing a Redis docker container and running it.  This is espically nice on windows because you don't have to worry about all the dependencies.

This guide assumes that you already have docker installed.

Run the following,

```
docker pull redis
docker run --name unique-name -d redis
```

This will expose port 6379 on your localhost.  You can now set your celery backend to `backend='redis://127.0.0.1'`.

[Source](https://koukia.ca/installing-redis-on-windows-using-docker-containers-7737d2ebc25e)

## Install rabbitmq docker image
Install a rabbitmy docker image by

`docker run -d --hostname flask-rabbit --name flask-rabbit -p 4369:4369 -p 5671:5671 -p 5672:5672 rabbitmq:3`

Then in your celery config set you broker as `broker='amqp://localhost:5672'`

[Source](https://docs.docker.com/samples/library/rabbitmq/)

## Start Celery workers

Run demo app:
`celery -A scripts.celery_demo worker -l info -P gevent`

To run the flask celery worker:
`celery -A app.entry_celery worker -l info -P gevent`