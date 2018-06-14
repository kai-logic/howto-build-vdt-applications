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

""" CollectionsView
    do operations to several collections at a time
    
    PUT will search for collections
"""


class CollectionView(JsonView):
    def get(self, request, collection_id: str) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)

            # Query parameters
            content = request.GET.get('content', None)
            field = request.GET.get('field', None)
            first = request.GET.get('first', None)
            number = request.GET.get('number', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            collection = vdt_python_sdk.get_collection(vsurl=settings.VSAPI_BASE, auth=auth,
                                                       collection_id=collection_id, first=first,
                                                       number=number, field=field, content=content,
                                                       accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return collection, 200


class CollectionsView(JsonView):
    def put(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Mandatory variables
            query = data['query']

            # Voluntary variables
            first = data.get('first', None)
            number = data.get('number', None)
            group = data.get('group', None)
            content = data.get('content', None)
            field = data.get('field', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        isd = collection_search_doc(query)

        try:
            collections = vdt_python_sdk.search_collections(vsurl=settings.VSAPI_BASE, auth=auth,
                                                            isd=isd, first=first, number=number,
                                                            group=group, content=content,
                                                            field=field, accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return collections, 200


def collection_search_doc(query: str=None) -> E.ItemSearchDocument():
    isd = E.ItemSearchDocument()
    top_level_and_op = E.operator(operation="AND")
    isd.append(top_level_and_op)

    if query:
        for term in query.split(','):
            top_level_and_op.append(E.text(term))
    return isd
