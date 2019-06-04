from flask import jsonify
from flask_restplus import Resource, Namespace, fields


from .tasks import add


api = Namespace('', description='Pywren Hello World API')


add_model = api.model(
    'Add Two Numbers', {
        'x': fields.Integer(),
        'y': fields.Integer()
    }
)


@api.route('/celery-add-start')
class CeleryAddStart(Resource):
    @api.expect(add_model)
    def post(self):

        data = api.payload
        x = data['x']
        y = data['y']
        task = add.apply_async((x, y))
        return jsonify({'task_id': task.id})


@api.route('/celery-add-results/<string:task_id>')
class CeleryAddGetResults(Resource):
    def get(self, task_id):
        task = add.AsyncResult(task_id)
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
