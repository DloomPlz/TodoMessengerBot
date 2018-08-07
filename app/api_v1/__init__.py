from flask import Blueprint

api = Blueprint('api_v1', __name__)

# Import any endpoints here to make them available
from . import webhook
from . import webhook_dev
