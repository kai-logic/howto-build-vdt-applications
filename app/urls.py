from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from django.contrib import admin
from django.views.generic import TemplateView
# Views
from .views import item, collection, job, library, shape, storage, vidispine

__author__ = 'anton'

admin.autodiscover()

urlpatterns = [
    path('<str>', TemplateView.as_view(template_name="index.html")),
    path('', TemplateView.as_view(template_name="index.html")),
    path('api/version', vidispine.VersionView.as_view(), name='version_json'),
    path('api/item/<str:item_id>', item.ItemView.as_view(), name='item_json'),
    path('api/items', item.ItemsView.as_view(), name='items_search_json'),
    path('api/collection/<str:collection_id>', collection.CollectionView.as_view(),
         name='get_collection'),
    path('api/collections', collection.CollectionsView.as_view(), name='collections_search_json'),
    path('api/job/<str:job_id>', job.JobView.as_view(), name='job_json'),
    path('api/jobs', job.JobsView.as_view(), name='jobs_search_json'),
    path('api/libraries', library.LibrariesView.as_view(), name='libraries_search_json'),
    path('api/shape-tag', shape.ShapeTagView.as_view(), name='shape_tags_json'),

    path('api/storages', storage.StoragesView.as_view(), name='storages_json'),
    path('api/storage/<str:storage_id>/importable', storage.StorageImportablesView.as_view(),
         name='storage_files_json'),
    path('api/storage/<str:storage_id>/file/<str:file_id>/import', storage.FileImportView.as_view(),
         name='start_file_import'),

    path('api/upload/passkey', job.WebuploadView.as_view(), name='get_upload_token'),

    path('api/resource', vidispine.ResourceView.as_view(), name='get_resources'),
    path('api/transcode', job.TranscodeView.as_view(), name='transcode'),
    path('api/vidinet/qc', job.VidinetQCView.as_view(), name='vidinet_qc'),

    path('api/export-location', vidispine.ExportView.as_view(), name='get_export_location'),
    path('api/shape-export', shape.ShapeExportView.as_view(), name='start_shape_export'),
]

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
