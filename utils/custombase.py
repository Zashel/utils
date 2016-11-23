class AttributedDict(dict):
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