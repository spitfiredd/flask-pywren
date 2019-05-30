import os
from time import sleep
from celery import Celery

import pywren_ibm_cloud as pywren


app = Celery('tasks',
             broker='amqp://localhost:5672',
             backend='redis://127.0.0.1')


def pywren_test():
    runtime = "spitfiredd/pywren-flaskapi-runtime:3.7"
    iterdata = [1, 2, 3, 4]

    PYWREN_CONFIG = {
        'pywren': {
            'storage_bucket': os.environ.get('PYWREN_STORAGE_BUCKET')
        },
        'ibm_cf': {
            'endpoint': os.environ.get('PYWREN_IBM_CF_ENDPOINT'),
            'namespace': os.environ.get('PYWREN_IBM_CF_NAMESPACE'),
            'api_key': os.environ.get('PYWREN_IBM_CF_API_KEY')
        },
        'ibm_cos': {
            'endpoint': os.environ.get('PYWREN_IBM_COS_ENDPOINT'),
            'api_key': os.environ.get('PYWREN_IBM_COS_API_KEY')
        }
    }

    def my_map_function(x):
        return x + 7

    def my_reduce_function(results):
        total = 0
        for map_result in results:
            total = total + map_result
        return total

    pw = pywren.ibm_cf_executor(config=PYWREN_CONFIG,
                                runtime=runtime)
    pw.map_reduce(my_map_function, iterdata, my_reduce_function)
    result = pw.get_result()
    return {'result': result}


@app.task
def pywren_task():
    sleep(6)
    return pywren_test()
