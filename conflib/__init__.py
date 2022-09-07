import json

class Config(object):
    def __init__(self, conf: dict):
        self.conf = conf
        for key in conf:
            Type = type(conf[key])
            if Type == dict:
                setattr(self, key, Config(conf[key]))
            else:
                setattr(self, key, conf[key])


    def dict(self):
        return self.conf


    def __getattr__(self, name):
        setattr(self, name, None)
        return None


class JsonConfig(object):
    def __init__(self, exist: str):
        with open(exist, 'r', encoding='utf-8') as file:
            self.raw = file.read()
            self.conf = json.loads(self.raw)

        for key in self.conf:
            Type = type(self.conf[key])
            if Type == dict:
                setattr(self, key, Config(self.conf[key]))
            else:
                setattr(self, key, self.conf[key])


    def dict(self):
        return self.conf


    def json(self):
        return self.conf


    def __getattr__(self, name):
        setattr(self, name, None)
        return None