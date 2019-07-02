import json
import os
from threading import Thread


class OrangeBase:

    def __setitem__(self, key, value):
        """set a new item to the database"""
        return self.set(key, value)

    def __getitem__(self, key):
        """get an item from the database"""
        return self.get(key)

    def __len__(self):
        """get the size of the database"""
        return len(self._db)

    def __delitem__(self, key):
        """delete an item from the database"""
        return self.delete(key)

    def __iter__(self):
        """make an iterable from the database"""
        return iter(self._db)

    def __contains__(self, key):
        """check whether database contains a key"""
        return self.has(key)

    def get(self, key, default=None):
        """
        get value assocaited with a key
        :param key: targeted key value
        :param default: default value
        :returns: value or default value
        """
        if key not in self._db:
            return default

        return self._db[key]

    def set(self, key, value, overwrite=True, dump=True):
        """
        set a new value for the given key
        :param key: targeted key
        :param value: associated value
        :param overwrite: would not overwrite if set to False
        :param dump: would not dump if set to True, for bulk set
        :returns True: on success
        """
        if not overwrite and key in self._db:
            return False

        self._db[key] = value
        self.dump(force=False)
        return True

    def setm(self, *args, overwrite=True):
        """
        set many new value and keys
        :param items: (key, value) tuples
        :param overwrite: would not overwrite if set to False
        :returns: True on success
        """
        for key, value in args:
            self.set(key, value, overwrite, False)

        self.dump(force=False)
        return True

    def delete(self, key):
        """
        delete the value associated with key
        :param key: targeted key
        :returns: True on success
        """
        if not key in self._db:
            return False

        del self._db[key]
        self.dump(force=False)
        return True

    def clear(self):
        """
        clear the entire database
        :returns: True on success
        """
        self._db.clear()
        self.dump(force=False)
        return True

    def has(self, key):
        """
        check whether a value exists in database
        :param key: targeted key
        :returns: True if key exists
        """
        return key in self._db

    def pop(self, key, default=None):
        """
        pop an item from the database
        :param key: targeted key
        :param default: default value
        :returns: value or default
        """
        value = self._db.pop(key, default)
        self.dump(force=False)
        return value

    def incrby(self, key, increment):
        """
        incremenet the interger value of the given field
        by the value of the given increment
        :param key: key of the given field
        :param incremenet: increment value
        :returns: True on success
        """
        if key not in self._db:
            return False

        value = self.get(key)
        if isinstance(value, int):
            value += increment
            self.set(key, value)
            return True

        return False

    def getm(self, *args, default=None):
        """
        get the values of the given fields
        in the same order as the keys
        :param keys: key parameteres
        :param default: default value when key does not exists
        :returns: ordered list of the values
        """
        return [self.get(key, default) for key in args]

    def setnx(self, key, value):
        """
        set the value for the given key only if the
        key does not already exits in the database
        :param key: targeted key
        :param value: associated value
        :returns: True if value was set
        """
        if key in self._db:
            return False

        self.set(key, value)
        return True

    def child(self, path):
        """
        initialize a new child database
        :param path: url like path for the child database
        :returns: child database instance
        """
        return OrangeChild(self, path)

    def lcreate(self, key):
        """
        create a new list
        :param key: targeted key
        :returns: True on success
        """
        return self.set(key, list())

    def lgetall(self, key):
        """
        get entire list
        :param key: list's key
        :returns: target list
        """
        return self[key]

    def lget(self, key, index):
        """
        get specific index from list
        :param key: list's key
        :param index: value's index
        :returns: targeted value
        """
        return self[key][index]

    def llen(self, key):
        """
        get list's size
        :param key: list's key
        :returns: list's size
        """
        return len(self[key])

    def lappend(self, key, value):
        """
        append a new value to a list
        :param key: list's key
        :param value: new value
        :returns: True on success
        """
        self._db[key].append(value)
        self.dump(force=False)
        return True

    def ldellist(self, key):
        """
        delete a list from the database
        :param key: list's key
        :returns: list's lenght
        """
        length = len(self.get(key))
        del self[key]
        return length

    def ldelvalue(self, key, value):
        """
        delete a value from list
        :param key: list's key
        :param value: targetd value
        :returns: True on success
        """
        self[key].remove(value)
        self.dump(force=False)
        return True

    def ldelindex(self, key, index):
        """
        delete a value from list by its index
        :param key: list's key
        :param index: value's index in list
        :returns: True on success
        """
        del self[key][index]
        self.dump(force=False)
        return True

    def lhas(self, key, value):
        """
        check whether a value exists in a list
        :param key: list's key
        :param value: targeted value
        :returns: True if exits
        """
        return value in self[key]

    def lextend(self, key, sec):
        """
        extend the list with a sequence
        :param key; list's key
        :param sec: new sequence
        :returns: True on success
        """
        self[key].extend(sec)
        self.dump(force=False)
        return True

    def lpop(self, key):
        """
        pop the last value in the list
        :param key: list's key
        :returns: popped value from list
        """
        val = self[key].pop()
        self.dump(force=False)
        return val

    def copy(self):
        """make a copy of the database's dictionary"""
        return self._db.copy()

    def keys(self):
        """:returns: a list of the keys in the database"""
        return self._db.keys()

    def values(self):
        """:returns: a list of the values in the database"""
        return self._db.values()

    def items(self):
        """:returns: returns a list of tuples of key values"""
        return self._db.items()


class Orange(OrangeBase):

    def __init__(self, file_path, auto_dump=True, load=True):
        """
        initialize a new Orange database
        :param file_path: path to the db file
        :param auto_dump: automatically store db on updates
        :param load: will load database if is True
        """
        self._file_path = os.path.expanduser(file_path)
        self._auto_dump = auto_dump
        self._db = None
        if load:
            self._load()

    def _load(self):
        """
        load the database from local storage
        :returns: True on success
        """
        if os.path.exists(self._file_path):
            try:
                self._db = json.load(open(self._file_path, "r"))
            except ValueError:
                # in case the file is empty
                self._db = dict()
        else:
            self._db = dict()
        return True

    def dump(self, force=True, path=None):
        """
        dumps the current database into the file
        :param force: if set to true would ignore _auto_dump value
        :param path: optional path could also be provided
        :returns: True on success
        """
        if force or self._auto_dump:
            path = os.path.expanduser(path) if path else self._file_path
            thread = Thread(target=json.dump,
                            args=(self._db, open(path, "w")))
            thread.start()
            thread.join()
            return True

        return False


class OrangeChild(OrangeBase):

    def __init__(self, parent, path):
        """
        initialize a new OrangeDB Child
        :param parent: parent Database
        :param path: child path, url formatted
        """
        self._path = OrangeChild._parse_path(path)
        if not self._path:
            raise Exception("path is not valid")

        self._parent = parent
        self._db = None
        self._load_child_db()

    @staticmethod
    def _parse_path(path):
        """ parses the path """
        if path.startswith('/'):
            path = path[1:]
        if path.endswith('/'):
            path = path[:-1]

        return path.split('/')

    def _load_child_db(self):
        """ process and load child db """
        curr_db = self._parent._db
        for div in self._path:
            if not div in curr_db:
                curr_db[div] = dict()
            curr_db = curr_db[div]
        self._db = curr_db

    def dump(self, *args, **kwargs):
        """ dumpt the child database """
        return self._parent.dump(*args, **kwargs)

    def clear(self):
        """ clear child database """
        parent = self._parent._db
        for div in self._path[:-1]:
            parent = parent[div]

        parent[self._path[-1]] = dict()
        self.dump(force=False)
        self._load_child_db()
        return True