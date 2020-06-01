#Singleton Config

import json

class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

@Singleton
class Config(Singleton):
    def __init__(self):
        self.demo = None

    def load(self, json_str=None, json_file=None):
        json_dict = dict()
        if json_file is not None:
            with open(json_file, 'r+', encoding = 'GBK') as f:
                json_dict = json.load(f)
        elif json_str is not None:
            json_dict = json.loads(json_str)

        attrs = dir(self)
        for attr in attrs:
            if attr in json_dict:
                setattr(self, attr, json_dict.get(attr))
