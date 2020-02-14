import json


# 公用的配置名
CONF_INIT = 'init'
CONF_DAY_START = 'day_start'
CONF_TASKS = 'tasks'


gInitConf = {
    CONF_DAY_START: (9*3600+30*60),     # 默认9:30
}


class Config(object):
    def __init__(self, filename):
        self.filename = filename
        self.config = {}
        self.load()
        self.init_conf()

    def get_conf(self, key, default=None):
        if key not in self.config:
            return default
        return self.config[key]

    def init_conf(self):
        # 最开始的初始化
        if self.get_conf(CONF_INIT):
            return
        for key, value in gInitConf.items():
            self.config[key] = value
        self.config[CONF_INIT] = True
        self.save()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                self.config = json.load(f)
        except:
            print('filename error while load')

    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.config, f)
        except:
            print('filename error while save')

    def save_conf(self, key, value):
        self.config[key] = value
        self.save()
