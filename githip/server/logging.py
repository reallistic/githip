import logging
import ujson
import traceback

from collections import OrderedDict

from sanic.log import log


json_dumps = ujson.dumps  # pylint: disable=no-member
json_loads = ujson.loads  # pylint: disable=no-member


class JSONFormatter(logging.Formatter):

    """Formatter that dumps the message to JSON"""

    _system_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    def __init__(self, app=None, pretty=False):
        super(JSONFormatter, self).__init__()
        self.app = app
        self.pretty = pretty

    def format(self, record):
        """Formats a log record as a JSON string"""
        indent = None
        if self.pretty or self.app.config.get('PRETTY_PRINT_LOGS'):
            indent = 4

        exc_info_text = None
        # Include the stacktrace if we're in debug mode.
        if self.app.config.get('DEBUG') and record.exc_info:
            exc_info_text = str(record.exc_info[1]) + '\n\n' + \
                ''.join(traceback.format_tb(record.exc_info[2]))

        if isinstance(record.msg, dict):
            data = record.msg
            if exc_info_text:
                data['Traceback'] = exc_info_text
            rv = json_dumps(data, sort_keys=False, indent=indent)
        else:
            # This line merges any user supplied arguments into the string via
            # interpolation.
            record.message = record.getMessage()

            if '%(asctime)' in self._system_fmt:
                record.asctime = self.formatTime(record)
            rv = self._system_fmt % record.__dict__

            if exc_info_text:
                rv += '\n\n%s' % exc_info_text

        return rv


def clean_dict(data):
    # support orderded dict
    rv = data.__class__()
    for key, val in data.items():
        if val is not None:
            rv[key] = val
    return rv


def get_request_log(request):
    rv = OrderedDict((
        ('method', request.method),
        ('path', request.path),
        ('json', request.json),
        ('args', request.raw_args or None),
        ('headers', dict(request.headers.items()) or None)
    ))

    rv = clean_dict(rv)

    return rv


def get_response_log(response):
    if getattr(response, 'log_json_response', False):
        if response.content_type == 'application/json':
            body = ('json', json_loads(response.body))
        else:
            body = ('body', response.body)
    else:
        body = '<REDACTED>'

    rv = OrderedDict((
        ('status', response.status),
        ('body', body),
        ('headers', dict(response.headers.items()) or None)
    ))

    rv = clean_dict(rv)

    return rv


def log_response(request, response):
    # The adapter adds contextual information to the record.
    log_entry = OrderedDict()
    log_entry['request'] = get_request_log(request)
    log_entry['response'] = get_response_log(response)
    log.info(log_entry)


def setup_logger(app):
    formatter = JSONFormatter(app, pretty=True)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(app.config.get('LOG_LEVEL'))
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)
    app.middleware('response')(log_response)
