__author__ = 'anton'

"""
A Storage object is like a dictionary except `obj.foo` can be used
in addition to `obj['foo']`.
"""


class Storage(dict):
    def __init__(self, *args, **kwargs):
        super(Storage, self).__init__(*args, **kwargs)
        for k, v in self.items():
            if isinstance(v, dict):
                self[k] = Storage(v)
            elif isinstance(v, list):
                for i, l in enumerate(v):
                    if isinstance(l, dict):
                        v[i] = Storage(l)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)
