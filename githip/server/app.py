import sys

from sanic import Sanic
from sanic.exceptions import SanicException
from sanic.log import log

from . import config, errors, routes, views, logging
from .response import make_json_response


def handle_server_error(request, exception):
    if exception.status_code == 500:
        log.error('App error %s', exception, exc_info=sys.exc_info())
        message = 'An unknown error occured'
    else:
        message = str(exception)
    return make_json_response(message=message,
                              status_code=exception.status_code)


def handle_api_error(request, exception):
    return exception.make_json_response()


def create_app():
    # Setup log level so sanic wont add its default handler
    log.setLevel(config.get('LOG_LEVEL'))

    app = Sanic(__name__, log_config=None)
    app.config.from_object(config.config)
    logging.setup_logger(app)

    app.blueprint(routes.blueprint)
    app.blueprint(views.blueprint)

    app.exception(SanicException)(handle_server_error)
    app.exception(errors.ApiError)(handle_api_error)

    app.static('/static', './githip/dist/static')

    return app
