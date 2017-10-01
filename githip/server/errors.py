from .response import make_json_response


class ApiError:

    msg_template = '%(message)s code=%(code)s status_code=%(status_code)s'

    def __init__(self, message, status_code=400, code='Error'):
        self.message = message
        self.status_code = status_code
        self.code = code

    def make_json_response(self, request):
        return make_json_response(message=self.message, code=self.code,
                                  request=request,
                                  status_code=self.status_code)

    def __str__(self):
        params = vars(self)
        return self.msg_template % params

    def __repr__(self):
        msg = str(self)
        return '<%s msg=%s>' % (self.__class__.__name__, msg)
