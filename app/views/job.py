# Settings
from django.conf import settings
# 3rd party helpers
from requests.exceptions import HTTPError
from typing import Tuple
from lxml.objectify import ElementMaker
import json
import random
import string
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


class JobView(JsonView):
    def get(self, request, job_id: str) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)

            # Query parameters
            metadata = request.GET.get('metadata', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            job = vdt_python_sdk.get_job(vsurl=settings.VSAPI_BASE, auth=auth, job_id=job_id,
                                         metadata=metadata, accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return job, 200

    def delete(self, request, job_id: str) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            job = vdt_python_sdk.delete_job(vsurl=settings.VSAPI_BASE, auth=auth, job_id=job_id)
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return job, 200


class JobsView(JsonView):
    def put(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Voluntary variables
            first = data.get('first', None)
            number = data.get('number', None)
            job_type = data.get('jobType', None)
            state = data.get('state', None)
            sort = data.get('sort', None)
            job_metadata = data.get('jobMetadata', None)
            metadata = data.get('metadata', None)
            starttime_from = data.get('starttimeFrom', None)
            starttime_to = data.get('starttimeTo', None)
            finishtime_from = data.get('finishtimeFrom', None)
            finishtime_to = data.get('finishtimeTo', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            jobs = vdt_python_sdk.get_jobs(vsurl=settings.VSAPI_BASE, auth=auth, first=first,
                                           number=number, job_type=job_type, state=state, sort=sort,
                                           job_metadata=job_metadata, metadata=metadata,
                                           starttime_from=starttime_from,
                                           starttime_to=starttime_to,
                                           finishtime_from=finishtime_from,
                                           finishtime_to=finishtime_to,
                                           accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return jobs, 200


class WebuploadView(JsonView):
    def get(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)

            filename = request.GET.get('filename', None)
            filesize = request.GET.get('filesize', None)
            collection_id = request.GET.get('collectionId', None)
            settings_id = request.GET.get('settingsId', None)
            tag = request.GET.get('tag', None)
        except KeyError:
            return Storage(dict(content="No auth")), 401
        except ValueError:
            raise Exception("Invalid request body or header")

        transfer_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                              for _ in range(10))

        try:
            document = vdt_python_sdk.get_upload_token(vsurl=settings.VSAPI_BASE,
                                                       auth=auth, transfer_id=transfer_id,
                                                       settings_id=settings_id, tag=tag,
                                                       filename=filename, filesize=filesize,
                                                       collection_id=collection_id)
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        passkey = None
        for data in document.data:
            if data.key == 'passkey':
                passkey = data.value

        if passkey is None:
            raise Exception("Failed to get upload token")

        return Storage(passkey=passkey, transferId=transfer_id), 200


# vidinet transcode jobs
class TranscodeView(JsonView):
    def get(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)

            # Voluntary variables
            item_id = request.GET.get('itemId', None)
            tag = request.GET.get('tag', None)
            existing_estimate = request.GET.get('existingEstimate', None)
        except ValueError:
            raise Exception("Invalid request body or header")

        if existing_estimate:
            cost = vdt_python_sdk.get_exact_url(vsurl=existing_estimate, auth=auth,
                                                accept='application/json')
        else:
            try:
                estimate = vdt_python_sdk.vidinet_cost_transcode(vsurl=settings.VSAPI_BASE,
                                                                 auth=auth,
                                                                 item_id=item_id, tag=tag,
                                                                 accept='application/json')
                cost = vdt_python_sdk.get_exact_url(vsurl=estimate.url, auth=auth,
                                                    accept='application/json')
            except HTTPError as e:
                return Storage(dict(url=e.request.path_url,
                                    message=e.response.content.decode(
                                        'utf-8'))), e.response.status_code

        return cost, 200

    def post(self, request):
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Voluntary variables
            item_id = data.get('itemId', None)
            tag = data.get('tag', None)
            resource_id = data.get('resourceId', None)
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            transcode = vdt_python_sdk.start_transcode(vsurl=settings.VSAPI_BASE, auth=auth,
                                                       item_id=item_id, tag=tag,
                                                       resource_id=resource_id,
                                                       accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return transcode, 200


# vidinet qc jobs
class VidinetQCView(JsonView):
    def get(self, request) -> responseBE:
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)

            # Voluntary variables
            item_id = request.GET.get('itemId', None)
            shape_id = request.GET.get('shapeId', None)
            resource_id = request.GET.get('resourceId', None)
            job_metadata = request.GET.get('jobmetadata', None)
            existing_estimate = request.GET.get('existingEstimate', None)
        except ValueError:
            raise Exception("Invalid request body or header")

        if existing_estimate:
            cost = vdt_python_sdk.get_exact_url(vsurl=existing_estimate, auth=auth,
                                                accept='application/json')
        else:
            try:
                estimate = vdt_python_sdk.vidinet_cost_qc(vsurl=settings.VSAPI_BASE,
                                                          auth=auth,
                                                          item_id=item_id, shape_id=shape_id,
                                                          resource_id=resource_id,
                                                          job_metadata=job_metadata,
                                                          accept='application/json')
                cost = vdt_python_sdk.get_exact_url(vsurl=estimate.url, auth=auth,
                                                    accept='application/json')
            except HTTPError as e:
                return Storage(dict(url=e.request.path_url,
                                    message=e.response.content.decode(
                                        'utf-8'))), e.response.status_code

        return cost, 200

    def post(self, request):
        try:
            auth = dict(username=settings.VS_USERNAME, password=settings.VS_PASSWORD)
            body = request.body.decode("utf-8")
            data = json.loads(body)

            # Voluntary variables
            item_id = data.get('itemId', None)
            shape_id = data.get('shapeId', None)
            resource_id = data.get('resourceId', None)
            job_metadata = data.get('jobmetadata', None)
        except ValueError:
            raise Exception("Invalid request body or header")

        try:
            transcode = vdt_python_sdk.start_qc(vsurl=settings.VSAPI_BASE, auth=auth,
                                                item_id=item_id, shape_id=shape_id,
                                                resource_id=resource_id,
                                                job_metadata=job_metadata,
                                                accept='application/json')
        except HTTPError as e:
            return Storage(dict(url=e.request.path_url,
                                message=e.response.content.decode('utf-8'))), e.response.status_code

        return transcode, 200
