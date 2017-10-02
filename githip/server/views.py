from sanic import Blueprint

blueprint = Blueprint(__name__)

blueprint.static('/', 'githip/client/build/index.html')
blueprint.static('/index.html', 'githip/client/build/index.html')
blueprint.static('/static', 'githip/client/build/static')
