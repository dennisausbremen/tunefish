# coding=utf-8

from flask import Response, jsonify
from flask.views import MethodView


AJAX_SUCCESS = Response(200)


class AjaxException(Exception):
    def __init__(self, *args):
        super(Exception, self).__init__()
        self.errors = args


class AjaxForm(MethodView):
    def on_submit(self):
        return AJAX_SUCCESS

    def post(self):
        if self.form.validate_on_submit():
            try:
                result = self.on_submit()
                if type(result) is Response:
                    return result
                else:
                    return jsonify(result)
            except AjaxException as e:
                errors = self.form.errors
                if len(e.errors) > 0:
                    errors['general'] = e.errors
                return jsonify(errors=errors), 400
        else:
            return jsonify(errors=self.form.errors), 400