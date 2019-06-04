from flask import jsonify, current_app as c_app
from flask_restplus import Resource, Namespace, fields

import pywren_ibm_cloud as pywren

from .models import my_map_function, my_reduce_function
from .tasks import pywren_long_task


api = Namespace('', description='Pywren Hello World API')

pywren_model = api.model(
    'Pywren Example Model', {
        'iterdata': fields.List(fields.Integer())
    }
)


@api.route('/pywren-hello-world')
class PywrenHello(Resource):
    @api.expect(pywren_model)
    def post(self):

        data = api.payload
        iterdata = data['iterdata']

        pw = pywren.ibm_cf_executor(config=c_app.config.get('PYWREN_CONFIG'),
                                    runtime=c_app.config.get('PYWREN_RUNTIME'))
        pw.map_reduce(my_map_function, iterdata, my_reduce_function)
        result = pw.get_result()
        return jsonify({'result': result})


@api.route('/pywren-hello-world-celery')
class PywrenHelloCelery(Resource):

    @api.expect(pywren_model)
    def post(self):

        data = api.payload
        iterdata = data['iterdata']

        task_kw = dict(
            iterdata=iterdata,
            config=c_app.config.get('PYWREN_CONFIG'),
            runtime=c_app.config.get('PYWREN_RUNTIME')
        )

        task = pywren_long_task.apply_async(kwargs=task_kw)

        return jsonify({'task_id': task.id})


@api.route('/pywren-hello-world-celery/<string:task_id>')
class PywrenHelloCeleryResults(Resource):

    def get(self, task_id):

        task = pywren_long_task.AsyncResult(task_id)

        if task.state == 'PENDING':
            resp = {'state': task.state}
        elif task.state == 'SUCCESS':
            resp = {
                'state': task.state,
                'result': task.get()
            }
        elif task.state == 'FAILURE':
            resp = {
                'state': task.state,
                'error': str(task.info)
            }

        return jsonify(resp)
