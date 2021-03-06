import random
from time import sleep
import pywren_ibm_cloud as pywren

from server.extensions import celery

# from .models import my_map_function, my_reduce_function


@celery.task
def pywren_long_task(iterdata=[], config=None, runtime=None):

    def my_map_function(x):
        return x + 7

    def my_reduce_function(results):
        total = 0
        for map_result in results:
            total = total + map_result
        return total

    pw = pywren.ibm_cf_executor(config=config, runtime=runtime)
    pw.map_reduce(my_map_function, iterdata, my_reduce_function)
    result = pw.get_result()

    # simulating a long task by sleeping n number of seconds before returning
    # the result
    n = random.randint(10, 40)
    sleep(n)
    return {'result': result}
