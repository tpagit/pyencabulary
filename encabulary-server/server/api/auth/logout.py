from flask import redirect
from flask.views import MethodView

from server.api.base.request import get_current_user_id, get_current_request
from server.api.base.response import ok_response
from server.database.management.db_manager import save_db_changes
from server.database.queries import get_db_user_by_id
from server.decorators.access_token_required import AccessTokenRequired


class LogoutAPI(MethodView):
    @AccessTokenRequired()
    def post(self):
        current_user_id = get_current_user_id()

        db_user = get_db_user_by_id(current_user_id)
        self._remove_user_session_and_access_token(db_user)

        request = get_current_request()
        if request.http_request.args.get('redirect', 'false') == 'true':
            response = redirect('/index')
        else:
            response = ok_response()

        response.set_cookie('access_token', '', expires=0)

        return response

    def _remove_user_session_and_access_token(self, db_user):
        if db_user is not None:
            db_user.id_session = None
            save_db_changes()
