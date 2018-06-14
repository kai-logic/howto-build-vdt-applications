# 3rd party helpers
import json
import functools
from django.http import HttpResponse
from django.views.generic import View
from requests import HTTPError
from django.http.response import HttpResponseBase
from datetime import datetime, date
from lxml import objectify

__author__ = 'anton'

""" json_view
    helpers to inject into API-call-classes

    JsonEncoder is a class that will encode json objects

    JsonResponse is a response that will be injected by most API-calls
"""


class JsonView(View):
    """ View class for returning JSON.
        Return `data`, `status_code` from your view method.
        :see: View
    """

    def dispatch(self, request, *args, **kwargs):
        try:
            # data, status_code = super(JsonView, self).dispatch(request, *args, **kwargs)
            # if isinstance(data, HttpResponseBase):
            #     return data
            response = super(JsonView, self).dispatch(request, *args, **kwargs)
            if isinstance(response, tuple):
                data, status_code = response
            else:
                data = response
                status_code = 200
        except HTTPError as e:
            try:
                data = e.response.json()
            except ValueError:
                data = e.response.text
            status_code = e.response.status_code

        # Change '*' in order to include only specific sites to do calls to this server
        if isinstance(data, HttpResponseBase):
            # Preflight response
            _, methods = data._headers.get('allow', ['', ''])
            data['Access-Control-Allow-Methods'] = methods
            data['Access-Control-Allow-Origin'] = '*'
            data['Access-Control-Allow-Headers'] = 'Content-Type'
            return data
        else:
            xhr_response = JsonResponse(data, status=status_code)
            xhr_response["Access-Control-Allow-Origin"] = '*'
            return xhr_response


class JsonEncoder(json.JSONEncoder):
    """
        Custom encoder for serializing dates and such.
    """

    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        elif obj.__class__.__name__ == '__proxy__':
            # ugettext_lazy
            return str(obj)
        elif hasattr(obj, '__json__'):
            return obj.__json__()
        elif isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, objectify.IntElement):
            return int(obj)
        elif isinstance(obj, (objectify.FloatElement, objectify.NumberElement)):
            return float(obj)
        elif isinstance(obj, objectify.ObjectifiedDataElement):
            return str(obj)
        return super(JsonEncoder, self).default(obj)


class JsonResponse(HttpResponse):
    def __init__(self, content, status=None, content_type='application/json; charset=utf-8'):
        super(JsonResponse, self).__init__(
            content=json.dumps(content, cls=JsonEncoder),
            status=status,
            content_type=content_type,
        )


# is not used?
class JsonResponse2(object):
    """
        JSON response decorator
    """

    def __init__(self, func):
        self.func = func
        functools.update_wrapper(self, func)

    def __call__(self, request, *args, **kwargs):
        try:
            data, status_code = self.func(request, *args, **kwargs)
            if isinstance(data, HttpResponseBase):
                return data
        except HTTPError as e:
            try:
                data = e.response.json()
            except ValueError:
                data = e.response.text
            status_code = e.response.status_code
        return JsonResponse(data, status=status_code)

# flake8: noqa
