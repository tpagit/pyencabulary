from flask import render_template, redirect
from flask.views import MethodView

from server.api.base.request import get_current_user_id


class IndexView(MethodView):
    def get(self):
        user_id = get_current_user_id()

        if not user_id:
            return render_template('index.html')

        return redirect('/learn')
