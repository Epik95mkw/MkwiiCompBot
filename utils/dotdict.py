
class DotDict(dict):
    def __init__(self, _dict):
        super(DotDict, self).__init__(_dict)
        for k, v in _dict.items():
            if isinstance(v, dict):
                self[k] = DotDict(v)
            if isinstance(v, list):
                self[k] = [DotDict(e) if type(e) is dict else e for e in v]

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

    def update_new(self, newdict):
        self.update((k, v) for k, v in newdict.items() if k not in self)
        for k, v in newdict.items():
            if isinstance(v, dict) and isinstance(self[k], dict):
                self[k].update_new(v)
