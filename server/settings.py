from environs import Env

env = Env()
env.read_env()

# Flask Settings
ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'

# Celery settings
CELERY_BROKER_URL = env.str('CELERY_BROKER_URL', default='amqp://localhost:5672')
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND', default='redis://127.0.0.1')
# CELERY_BROKER_URL = 'amqp://localhost:5672'
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1'

# Pywren Settings
PYWREN_STORAGE_BUCKET = env.str('PYWREN_STORAGE_BUCKET', default='')
PYWREN_IBM_CF_ENDPOINT = env.str('PYWREN_IBM_CF_ENDPOINT', default='')
PYWREN_IBM_CF_NAMESPACE = env.str('PYWREN_IBM_CF_NAMESPACE', default='')
PYWREN_IBM_CF_API_KEY = env.str('PYWREN_IBM_CF_API_KEY', default='')
PYWREN_IBM_COS_ENDPOINT = env.str('PYWREN_IBM_COS_ENDPOINT', default='')
PYWREN_IBM_COS_API_KEY = env.str('PYWREN_IBM_COS_API_KEY', default='')
PYWREN_RUNTIME = "spitfiredd/pywren-flaskapi-runtime:3.7"

PYWREN_CONFIG = {
    'pywren': {
        'storage_bucket': PYWREN_STORAGE_BUCKET
    },
    'ibm_cf': {
        'endpoint': PYWREN_IBM_CF_ENDPOINT,
        'namespace': PYWREN_IBM_CF_NAMESPACE,
        'api_key': PYWREN_IBM_CF_API_KEY
    },
    'ibm_cos': {
        'endpoint': PYWREN_IBM_COS_ENDPOINT,
        'api_key': PYWREN_IBM_COS_API_KEY
    }
}
