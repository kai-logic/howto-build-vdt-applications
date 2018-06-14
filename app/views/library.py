# Settings
from django.conf import settings
# 3rd party helpers
from requests.exceptions import HTTPError
from typing import Tuple
from lxml.objectify import ElementMaker
import json
# Views
from .utils import Storage
from .json_view import JsonView
# VDT BE Components
from vdt_python_sdk.views import vdt_python_sdk

E = ElementMaker(namespace="http://xml.vidispine.com/schema/vidispine", annotate=False,
                 nsmap={"vs": "http://xml.vidispine.com/schema/vidispine"})

# Unified responses:
responseBE = Tuple[Storage, int]

__author__ = 'anton'

""" LibraryView
    some of the typical API-calls are used here
"""


class LibrariesView(JsonView):
    def put(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Voluntary variables
            first = data.get('first', None)
            number = data.get('number', None)
            auto_refresh = data.get('autoRefresh', None)
            frequency_from = data.get('frequencyFrom', None)
            frequency_to = data.get('frequencyTo', None)
            update_mode = data.get('updateMode', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            libraries = vdt_python_sdk.get_libraries(vsurl=settings.VSAPI_BASE, auth=auth,
                                                     first=first, number=number,
                                                     auto_refresh=auto_refresh,
                                                     frequency_from=frequency_from,
                                                     frequency_to=frequency_to,
                                                     update_mode=update_mode,
                                                     accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return libraries, 200
