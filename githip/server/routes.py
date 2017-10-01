from sanic import Blueprint

from .response import make_json_response

blueprint = Blueprint(__name__, url_prefix='/api')


@blueprint.route('/organization', methods=['GET'])
async def get_org_data(_):
    return make_json_response(**dict(hello='world'))
