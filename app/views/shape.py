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

""" JobView
    some of the typical API-calls are used here
"""


class ShapeTagView(JsonView):
    def get(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)

            # Query parameters
            url = request.GET.get('url', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            shape_tags = vdt_python_sdk.get_shape_tags(vsurl=settings.VSAPI_BASE, auth=auth,
                                                       the_url=url, accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return shape_tags, 200


class ShapeExportView(JsonView):
    def post(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Voluntary variables
            item_id = data.get('itemId', None)
            shape_id = data.get('shapeId', None)
            location_name = data.get('locationName', None)
            use_original_filename = data.get('useOriginalFilename', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            shape_export = vdt_python_sdk.start_shape_export(vsurl=settings.VSAPI_BASE, auth=auth,
                                                             item_id=item_id, shape_id=shape_id,
                                                             location_name=location_name,
                                                             use_original_filename=use_original_filename,
                                                             accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return shape_export, 200
