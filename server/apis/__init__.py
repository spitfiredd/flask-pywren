from flask import Blueprint
from flask_restplus import Api
from jsonschema import FormatChecker

from .pywren.routes import api as pywren_ns
from .hello.routes import api as add_ns

format_checker = FormatChecker(formats=["date"])

api_v1_bp = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(
    api_v1_bp,
    title='My Title',
    version='1.0',
    description='A description',
    format_checker=format_checker
)

api.add_namespace(pywren_ns)
api.add_namespace(add_ns)
