#  Example Pywren Flask REST API
Pywren Hello World REST API.

There are three routes in this example,

* POST /pywren-hello-world
* POST /pywren-hello-world-celery
* GET  /pywren-hello-world-celery/{task_id}

Navigate to `localhost:5000` and you can test these routes with swaggar.  The `/pywren-hello-world-celery` will return a `task_id` which you can copy/paste (copy withough the quotes) in `/pywren-hello-world-celery/{task_id}` which will return the result.

The basis for the example routes can be found [here](https://github.com/pywren/pywren-ibm-cloud/blob/master/examples/map_reduce.py).


## Getting Started
Quickly set up an environment by running `pipenv install` and `pipenv install --dev`. The `--dev` flag will add linting, testing and an ipython terminal.

## Setting up Pywren
Either in a `.env` file or by setting environ variables add the following,

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
You can process the endpoints with CURL or with python using the requests library, here is a simple example with requests.

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

Check out this [SO](https://stackoverflow.com/a/47331438/1761521) to see to to run Celery 4.3 in Windows 10.

Run demo app:
`celery -A scripts.celery_demo worker -l info -P gevent`

To run the flask celery worker:
`celery -A celery_entrypoint worker -l info -P gevent`

## TODO

* Add docker-compose file
