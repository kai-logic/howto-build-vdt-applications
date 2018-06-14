Item
====

Class ItemView
--------------

---
GET
---

Will return a specific item.

Get item. query parameter format::

    ?key1=value1,value2&key2=value3

Voluntary query parameters::

    fieldPath = str - Only include the specified fields, from the -INF to +INF metadata.
    contentPath = str - Include the specified fields, could be content in shapes, metadata or thumbnails.
    content = str - Include arbitrary amount of keys: metadata, uri, shape, poster, thumbnail, access, merged-access, external.
    field = str - Include metadata fields.

---
PUT
---

Will add or change the specific item metadata-field value.

Change item metadata field value. Input::

    {key: value}

Mandatory keys::

    name = str - Name of the field you want to change.
    value = str - Value of the field you want to change.


Class ItemsView
---------------

---
PUT
---

Search for items. Input::

    {key: value}

Voluntary keys::

    query = str - Comma separated search query.
    first = int - Include the items after this index.
    number = int - Include this amount of items in the result.
    group = str - Include the group.
    fieldPath = str - Only include the specified fields, from the -INF to +INF metadata.
    contentPath = str - Include the specified fields, could be content in shapes, metadata or thumbnails.
    content = str - Include arbitrary amount of keys: metadata, uri, shape, poster, thumbnail, access, merged-access, external.
    field = str - Include metadata fields.
    library = bool - The result will become a library if True, default is False.

