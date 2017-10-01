from sanic.log import log
from githip.server import create_app, config


def serve(app):
    port = config.get('PORT')

    try:
        log.info('serviing http app')
        app.run('0.0.0.0', port=port, debug=config.get('DEBUG'),
                log_config=False, workers=config.get('WORKER_COUNT'))
    except KeyboardInterrupt:
        log.info('Closing thread')


if __name__ == '__main__':
    serve(create_app())
