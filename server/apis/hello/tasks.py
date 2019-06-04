from time import sleep
from server.extensions import celery


@celery.task
def add(x, y):
    sleep(10)
    return x + y
