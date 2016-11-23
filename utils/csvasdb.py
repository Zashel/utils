from collections import UserDict
import os
#TODO Searches
#TODO Filters
#TODO Iters

class CsvAsDb():
    """Uses a CSV file as a DataBase"""
    def __init__(self, file_path, *, separator="\t", headers=None, index=list()):
        """Initializes the Dictionary"""
        self._file_path = file_path
        self._separator = separator
        self._headers = headers
        self._with_headers = headers is not None
        self._dir_headers = list()
        self._data = dict()
        self._new_files = int()
        self._active_row = None
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
            with open(self._file_path, "r") as index_file:
                self._index = [index.strip("\n").strip("\r") for index in index_file]
        self.read()

    def __dir__(self):
        directory = dir(super())
        directory.extend(self._dir_headers)
        return directory

    def __getattr__(self, item):
        if item in self._dir_headers and self._active_row is not None:
            return self._data[self._active_row][self._headers[self._dir_headers.index(item)]]
        else:
            raise AttributeError()

    def __getitem__(self, item):
        if item in self._data:
            self.set_index(item)
            return self
        else:
            KeyError

    def _set_index(self, field, data, index):
        """Includes a field/value index.
        To not to be repeated"""
        if field not in self._indexes:
            self._indexes[field] = dict()
        if data not in self._indexes[field]:
            self._indexes[field][data] = list()
        self._indexes[field][data].append(index)

    def del_index(self, field):
        """Delete an index. Why should you?"""
        if field in self._index:
            self._index.remove(field)
            del(self._indexes[field])

    def del_row(self, index=None):
        """Delete a row with a given index or the active one if not indicated"""
        if index is None:
            index = self._active_row
            self._active_row = None
        for head in self._index:
            self.indexes[head][self._data[index][head]].remove(index)
            if self.indexes[head][self._data[index][head]] == list():
                del(self.indexes[head][self._data[index][head]])
        del[self._data[index]]

    def insert_row(self, row):
        """Inserts data given a specific dictionary.
        Headers not coincident will be ignored"""
        index = "N{}".format(str(self._new_files))
        self._new_files += 1
        data = dict()
        for field in self._headers:
            try:
                data[field] = row[field]
            except KeyError:
                data[field] = str()
            if field in self._index:
                self._set_index(field, data[field], index)
        self._data[index] = data
        return index #Let's give the index of that new row

    def set_active(self, index):
        """Activates a specific row"""
        if index in self._data:
            self._active_row = index
        else:
            raise IndexError()

    def set_index(self, field):
        """Sets new index. Slow, slow."""
        if field in self._headers and field not in self._index:
            self._index.append(field)
            for index in self._data:
                self._set_index(field, self._data[index][field], index)

    def read(self):
        """Read the associated file and creates the dictionary"""
        with open(self._file_path, "r") as data_file:
            for index, row in enumerate(data_file):
                row = row.strip("\n").strip("\r").split(self._separator)
                if index == 0 and self._headers is None:
                    self._headers = row
                    self._dir_headers = [head.replace(" ", "_") for head in self._headers]
                else:
                    data = {}
                    for field_index, field in enumerate(self._headers):
                        data[field] = row[field_index]
                        if field in self._index:
                            self._set_index(field, row[field_index], index)
                    self._data[str(index)] = data #Change to str to be able to be ordered

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