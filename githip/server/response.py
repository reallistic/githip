import ujson

from sanic.response import HTTPResponse

json_dumps = ujson.dumps  # pylint: disable=no-member
json_loads = ujson.loads  # pylint: disable=no-member


def make_json_response(**kwargs):
    status = kwargs.pop('status_code', 200)
    log_json_response = kwargs.pop('log_json_response', True)
    headers = kwargs.pop('headers', None)

    resp = HTTPResponse(json_dumps(kwargs), headers=headers,
                        status=status, content_type="application/json")
    resp.log_json_response = log_json_response

    return resp
