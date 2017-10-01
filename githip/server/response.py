import ujson

from jinja2 import Environment, PackageLoader, select_autoescape

from sanic.response import HTTPResponse

json_dumps = ujson.dumps  # pylint: disable=no-member
json_loads = ujson.loads  # pylint: disable=no-member


template_env = Environment(
    loader=PackageLoader('githip.server', 'templates'),
    autoescape=select_autoescape(['html', 'xml']),
    enable_async=True
)


def make_json_response(**kwargs):
    status = kwargs.pop('status_code', 200)
    log_json_response = kwargs.pop('log_json_response', True)
    headers = kwargs.pop('headers', None)

    resp = HTTPResponse(json_dumps(kwargs), headers=headers,
                        status=status, content_type="application/json")
    resp.log_json_response = log_json_response

    return resp


async def render_template(template_name, **kwargs):
    status = kwargs.pop('status_code', 200)
    headers = kwargs.pop('headers', None)

    template = template_env.get_template(template_name)
    rendered_template = await template.render_async(**kwargs)

    resp = HTTPResponse(rendered_template, headers=headers, status=status,
                        content_type="text/html; charset=utf-8")
    resp.log_json_response = False

    return resp
