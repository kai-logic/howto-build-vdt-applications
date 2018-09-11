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

""" StorageView
    some of the typical API-calls are used here
"""


class StoragesView(JsonView):
    def get(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)

            # Query parameters
            status = request.GET.get('status', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            storages = vdt_python_sdk.get_storages(vsurl=settings.VSAPI_BASE, auth=auth,
                                                   status=status,
                                                   accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return storages, 200


class StorageImportablesView(JsonView):
    def get(self, request, storage_id: str) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            matrix_params = json.loads(request.GET.get('matrix'))
            first = matrix_params.get('first', None)
            number = matrix_params.get('number', None)
            state = matrix_params.get('state', 'CLOSED')
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            files = vdt_python_sdk.get_storage_importable(vsurl=settings.VSAPI_BASE, auth=auth,
                                                          storage_id=storage_id, state=state,
                                                          first=first, number=number,
                                                          accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        returned_files = []
        for file in files['element']:
            if file['file']['state'] == 'CLOSED':
                returned_files.append(file)
        files['element'] = returned_files
        return files, 200


class FileImportView(JsonView):
    def post(self, request, storage_id: str, file_id: str) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Voluntary variables
            tag = data.get('tag', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            file_import = vdt_python_sdk.start_file_import(vsurl=settings.VSAPI_BASE, auth=auth,
                                                           storage_id=storage_id, file_id=file_id,
                                                           tag=tag,
                                                           accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return file_import, 200
