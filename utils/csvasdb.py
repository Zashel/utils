from collections import UserDict
import os

class CsvAsDb():
    """Uses a CSV file as a DataBase"""
    def __init__(self, file_path, *, separator="\t", headers=None, index=list()):
        """Initializes the Dictionary"""
        self._file_path = file_path
        self._separator = separator
        self._headers = headers
        self._with_headers = headers is None and False or True
        self._dir_headers = list()
        self._data = dict()
        if not os.path.exists(self._file_path):
            os.makedirs(os.path.dirname(self._file_path))
        with open(self._file_path, "wb") as data_file:
            pass #A weird but valid way to create a file
        self._index = index
        self._indexes = dict()
        head, tail = os.path.split(os.path.basename(self._file_path))
        self._index_file = os.path.join(os.path.dirname(self._file_path), "{}.index".format(head))
        if self._index is list():
            if not os.path.exists(self._index_file):
                with open(self._file_path, "wb") as index_file:
                    pass #Again
            with open(self._file_path, "wb") as index_file:
                self._index = [index.strip("\n").strip("\r") for index in index_file]
        self.read()

    def __dir__(self):
        directory = dir(super())
        directory.extend(self._dir_headers)
        return directory

    def _set_index(self, field, data, index):
        if field not in self._indexes:
            self._indexes[field] = dict()
        if self._data[field] not in self._indexes[field]:
            self._indexes[field][data] = list()
        self._indexes[field][data].append(index)

    def del_index(self, field):
        """Delete an index. Why should you?"""
        if field in self._index:
            self._index.remove(field)
            del(self._indexes[field])

    def set_index(self, field):
        """Sets new index. Slow, slow."""
        if field in self._headers and field not in self._index:
            self._index.append(field)
            for index in self._data:
                self._set_index(field, self._data[index][field], index)

    def read(self):
        """Read the associated file and creates the dictionary"""
        with open(self._file_path, "rb") as data_file:
            for index, row in data_file:
                row = row.strip("\n").strip("\r").split(self._separator)
                if index == 0 and self._with_headers is False:
                    self._headers = row
                    self._dir_headers = [head.replace(" ", "_") for head in self._headers]
                else:
                    data = {}
                    for field, head in self._headers:
                        data[head] = row[field]
                        if head in self._index:
                            self._set_index(head, row[field], index)
                    self._data[index] = data

    def write(self, headers=None):
        """Writes the data to associated file and associated indexes"""
        order = [key for key in self._data]
        order.sort()
        final_data = str()
        if (headers is None and self._with_headers is True) or headers is True:
            final_data = self._separator.join(self._headers)
        final_data = "".join([final_data, "\n".join([self.separator.join(self._data[ord]) for ord in order])])
        final_index = "\n".join(self._index)
        with open(self._file_path, "wb") as data_file:
            data_file.write(final_data)
        with open(self._index_file, "wb") as index_file:
            index_file.write(final_index)