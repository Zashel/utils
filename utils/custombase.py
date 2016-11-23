class AttributedDict(dict):
    def __dir__(self):
        directory = dir(super())
        directory.extend([str(key for key in self)])
        return directory

    def __getattr__(self, attr):
        if attr in self:
            return self[attr]
        else:
            raise AttributeError

    def __setattr__(self, attr, value):
        if attr in self:
            self[attr] = value
        else:
            raise AttributeError