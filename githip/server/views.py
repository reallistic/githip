from sanic import Blueprint
from .response import render_template

blueprint = Blueprint(__name__)


@blueprint.route('/', methods=['GET'])
@blueprint.route('/<path>', methods=['GET'])
async def get_view(*_, path=None):
    return await render_template('index.html')
