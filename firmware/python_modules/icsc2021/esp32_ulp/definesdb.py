import os
import valuestore

DBNAME = 'defines.db'


class DefinesDB:
    def __init__(self):
        self._file = None
        self._db = None
        self._db_exists = None

    def clear(self):
        self.close()
        try:
            valuestore.save("system", "ulp_defines", {})
            self._db_exists = False
        except OSError:
            pass

    def is_open(self):
        return self._db is not None

    def open(self):
        if self.is_open():
            return
        try:
            self._db = valuestore.load("system", "ulp_defines")
        except :
            self._db = {}
        self._db_exists = True

    def close(self):
        if not self.is_open():
            return
        self._db = None

    def update(self, dictionary):
        for k, v in dictionary.items():
            self.__setitem__(k, v)

    def get(self, key, default):
        try:
            result = self.__getitem__(key)
        except KeyError:
            result = default
        return result

    def keys(self):
        self.open()
        return [k.decode() for k in self._db.keys()]

    def __getitem__(self, key):
        self.open()
        return self._db[key.encode()].decode()

    def __setitem__(self, key, value):
        self.open()
        self._db[key.encode()] = str(value).encode()
        valuestore.save("system", "ulp_defines", self._db)

    def __iter__(self):
        return iter(self.keys())
