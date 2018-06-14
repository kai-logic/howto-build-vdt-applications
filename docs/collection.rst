Collection
==========

Class CollectionsView
---------------------

---
PUT
---

Search for collections. Input::

    {key: value}

Voluntary keys::

    query = str - Comma separated search query.
    first = int - Include the collections after this index.
    number = int - Include this amount of collections in the result.
    group = str - Include the group.
    content = str - Include arbitrary amount of keys: metadata, uri, shape, poster, thumbnail, access, merged-access, external.
    field = str - Include metadata fields.

