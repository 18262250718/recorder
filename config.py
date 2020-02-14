import json


class Config(object):
    def __init__(self, filename):
        self.filename = filename
        self.config = {}
        try:
            with open(filename, 'r') as f:
                self.config = json.load(f)
        except:
            print('filename error while load')

    def get_conf(self, key):
        if key not  in self.config:
            return None
        return self.config[key]

    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.config, f)
        except:
            print('filename error while save')

    def save_conf(self, key, value):
        self.config[key] = value
        self.save()
