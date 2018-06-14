Library
=======

Class LibraryView
-----------------

---
GET
---

Will return a specific library.

---
PUT
---

Will add or change the specific library metadata-field value.

Class LibrariesView
-------------------

---
PUT
---

Search for Libraries. Input::

    {key: value}

Voluntary keys::

    first = int - Include the Libraries after this index.
    number = int - Include this amount of libraries in the result.
    autoRefresh = bool - Only list libraries with the specified auto refresh status.
    frequencyFrom = str - Only list libraries whose update frequency is greater than it.
    frequencyTo = str - Only list libraries whose update frequency is less than it.
    updateMode = str - Only list libraries with the specified update mode.

