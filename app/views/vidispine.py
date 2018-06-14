# Settings
from django.conf import settings
# 3rd party helpers
from requests.exceptions import HTTPError
from typing import Tuple
import json
# Views
from .utils import Storage
from .json_view import JsonView
# VDT BE Components
from vdt_python_sdk.views import vdt_python_sdk

# Unified responses:
responseBE = Tuple[Storage, int]

__author__ = 'anton'

"""
    some of the typical API-calls are used here
"""


class VersionView(JsonView):
    def get(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            version = vdt_python_sdk.version(vsurl=settings.VSAPI_BASE, auth=auth,
                                             accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return version, 200

    def put(self, request) -> responseBE:
        try:
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Mandatory variables
            username = data['username']
            password = data['password']
            auth = dict(username=username, password=password)
            auto_refresh = data.get('autoRefresh', None)
            seconds = data.get('seconds', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            token = vdt_python_sdk.get_token(vsurl=settings.VSAPI_BASE, auth=auth,
                                             auto_refresh=auto_refresh, seconds=seconds,
                                             username=username)
        except HTTPError:
            return Storage(dict(content='Incorrect username or password')), 401

        vs_token = token.text.decode("utf-8")

        auth = {
            'username': username,
            'token': vs_token
        }
        request.session['auth'] = auth

        return Storage(content='Successful login'), 200

    def delete(self, request) -> responseBE:
        request.session.flush()
        return Storage(content='Successful logout'), 200


class ResourceView(JsonView):
    def get(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)

            # Voluntary variables
            resource_type = request.GET.get('resourceType', None)
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            cost = vdt_python_sdk.get_resources(vsurl=settings.VSAPI_BASE, auth=auth,
                                                resource_type=resource_type,
                                                accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return cost, 200


class ExportView(JsonView):
    def get(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            export_locations = vdt_python_sdk.get_export_locations(vsurl=settings.VSAPI_BASE,
                                                                   auth=auth,
                                                                   accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return export_locations, 200
