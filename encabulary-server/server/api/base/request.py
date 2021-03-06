from flask import request
from jose import exceptions as jose_ex

import server.database.queries as db_query
from server.tools import types
from server.tools.jwt import Jwt


class BaseRequestDecorator:
    """Base flask request wrapper"""

    def __init__(self, http_request):
        self.http_request = http_request

    def get_value(self, field):
        raise NotImplementedError

    def get_string(self, field):
        """:rtype: str"""

        return types.to_string(self.get_value(field), default_value=None)

    def get_int(self, field):
        """:rtype: int"""

        return types.to_int(self.get_value(field), default_value=None)

    def get_float(self, field):
        """:rtype: float"""

        return types.to_float(self.get_value(field), default_value=None)

    def get_obj_list(self, field):
        """:rtype: list"""
        result = []

        values = self.get_value(field)

        if types.is_none_or_empty(values):
            return result

        return values

    def get_user_agent_platform(self):
        return self.http_request.user_agent.platform

    def is_from_mobile_device(self):
        phones = ['android', 'iphone', 'ipad']

        return self.get_user_agent_platform() in phones


class FormRequestDecorator(BaseRequestDecorator):
    """Form url encoded flask request wrapper"""

    def get_value(self, field):
        """:rtype: str"""

        if self.http_request.method == 'GET':
            value = self.http_request.args.get(field)
        else:
            value = self.http_request.form.get(field)

        if not types.is_none_or_empty(value):
            if type(value) is str:
                return value.strip()
            return value

        return None

    def __init__(self, http_request):
        super().__init__(http_request)


class JsonRequestDecorator(BaseRequestDecorator):
    """Json flask request wrapper"""

    def get_value(self, field):
        """:rtype: str"""

        if self.json_request is None and self.http_request.data:
            self.json_request = self.http_request.get_json()

        if self.json_request is None:
            return None

        value = self.json_request.get(field)

        if not types.is_none_or_empty(value):
            if type(value) is str:
                return value.strip()
            return value

        return None

    def __init__(self, http_request):
        super().__init__(http_request)

        self.json_request = None


class JQueryDataTableRequestDecorator(FormRequestDecorator):
    def __init__(self, http_request):
        super().__init__(http_request)

        self.draw = self.get_string('draw')
        self.skip = self.get_int('start')
        self.limit = self.get_int('length')
        self.order_column = self.get_string('order[0][column]')
        self.order_by = self.get_string('columns[{}][data]'.format(self.order_column))
        self.order_dir = self.get_string('order[0][dir]') or 'asc'
        self.filter_by = self.get_string('search[value]')


class RequestDecoratorFactory:
    @staticmethod
    def get_request(http_request):
        """
        :rtype: BaseRequestDecorator
        """

        if http_request is None:
            return BaseRequestDecorator(None)

        if 'Content-Type' in http_request.headers:
            if 'application/json' in http_request.headers['Content-Type']:
                return JsonRequestDecorator(http_request)

        if 'jqdatatable' in http_request.url:
            return JQueryDataTableRequestDecorator(request)

        return FormRequestDecorator(http_request)


def get_current_request():
    return RequestDecoratorFactory.get_request(request)


def get_current_user_id():
    token = get_current_request_token(silent=True)
    if token is None:
        return None

    return token.user_id


def get_current_request_token(silent=True):
    """
    Get current token
    :param silent: False - without raising exceptions
    :return: Jwt or None
    """

    if not silent:
        return Jwt.from_http_request(request)

    try:
        return Jwt.from_http_request(request)
    except (ValueError, jose_ex.ExpiredSignatureError, jose_ex.JWTError):
        return None


def is_authenticated():
    try:
        token = get_current_request_token(silent=False)
    except (ValueError, jose_ex.ExpiredSignatureError, jose_ex.JWTError):
        return False

    db_user = db_query.get_db_user_by_id(token.user_id)
    if db_user.id_session is None:
        return False

    if db_user.id_session != token.session_id:
        return False

    return True
