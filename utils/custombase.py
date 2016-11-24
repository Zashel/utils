class AttributedDict(dict):
    def __dir__(self):
        directory = dir(super())
        directory.extend([str(key.replace(" ", "_")) for key in self])
        return directory

    def __getattr__(self, attr):
        _dir_dict = dict()
        [_dir_dict.update({key.replace(" ", "_"): key}) for key in self]
        if attr in _dir_dict:
            return self[_dir_dict[attr]]
        else:
            raise AttributeError(attr)

    def __setattr__(self, attr, value):
        _dir_dict = dict()
        [_dir_dict.update({key.replace(" ", "_"): key}) for key in self]
        if attr in _dir_dict:
            self[_dir_dict[attr]] = value
        elif attr in self:
            self[attr] = value
        else:
            raise AttributeError(attr)
