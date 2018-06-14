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

""" ItemView
    some of the typical API-calls are used here
"""


class ItemView(JsonView):
    def get(self, request, item_id: str) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)

            # Query parameters
            content_path = request.GET.get('contentPath', None)
            field_path = request.GET.get('fieldPath', None)
            content = request.GET.get('content', None)
            field = request.GET.get('field', None)
            tag = request.GET.get('tag', None)
            method_type = request.GET.get('methodType', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        path = combine_paths(content_path, field_path)

        try:
            item = vdt_python_sdk.get_item(vsurl=settings.VSAPI_BASE, auth=auth, item_id=item_id,
                                           path=path, content=content, field=field, tag=tag,
                                           method_type=method_type, accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return item, 200

    def put(self, request, item_id: str) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Mandatory variables
            name = data['name']
            value = data['value']
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            item = vdt_python_sdk.put_item_metadata(vsurl=settings.VSAPI_BASE, auth=auth,
                                                    item_id=item_id, name=name, value=value,
                                                    accept='application/json',
                                                    content_type='application/xml')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return item, 200


class ItemsView(JsonView):
    def put(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Voluntary variables
            query = data.get('query', '')
            first = data.get('first', None)
            number = data.get('number', None)
            group = data.get('group', None)
            content_path = data.get('contentPath', None)
            field_path = data.get('fieldPath', None)
            content = data.get('content', None)
            field = data.get('field', None)
            library = data.get('library', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        isd = item_search_doc(query)

        path = combine_paths(content_path, field_path)

        try:
            items = vdt_python_sdk.search_items(vsurl=settings.VSAPI_BASE, auth=auth, isd=isd,
                                                first=first, number=number, group=group, path=path,
                                                content=content, field=field, library=library,
                                                accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return items, 200


def item_search_doc(query: str=None) -> E.ItemSearchDocument():
    isd = E.ItemSearchDocument()
    top_level_and_op = E.operator(operation="AND")
    isd.append(top_level_and_op)

    if query:
        for term in query.split(','):
            top_level_and_op.append(E.text(term))
    return isd


def combine_paths(content_path: str=None, field_path: str=None) -> str:
    path = content_path
    if field_path:
        field_paths = field_path.split(',')
        final_field_paths = []
        for f_path in field_paths:
            final_field_paths.append('v({})'.format(f_path))
        path = ','.join(final_field_paths + content_path.split(','))
    return path
