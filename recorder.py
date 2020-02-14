from config import *
import time
import json
"""
    记录、保存、加载
"""


class Recorder(object):
    def __init__(self, config):
        self.config = config
        self._day_start = config.get_conf(CONF_DAY_START)      # 一天中的开工时间 s
        self.datas = {}       # { day: [task_info, task_info]  }
        self.load_day_data(self.get_today_day())
        # 计数添加次数，用于判断能不能继续cancel
        self._last_adds = []

    def get_today_day(self):
        day_time = time.strftime("%Y-%m-%d", time.localtime(time.time()-self._day_start))
        return day_time

    def get_filename(self, day):
        return '{}.dat'.format(day)

    def load_day_data(self, day): # day 2020-02-02
        filename = self.get_filename(day)
        data = []
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
        except:
            pass
        self.datas[day] = data

    def save(self, record_day=None):
        for day, data in self.datas.items():
            if record_day is not None and day != record_day:
                continue
            filename = self.get_filename(day)
            try:
                with open(filename, 'w') as f:
                    json.dump(data, f)
            except:
                print('filename err while save recorders {}'.format(filename))

    def add_recorder(self, day, record):
        if day not in self.datas:
            self.load_day_data(day)
        self.datas[day].append(record)
        self._last_adds.append(day)
        self.save(day)

    def cancel_record(self):
        if len(self._last_adds) <= 0:
            return
        last_add_day = self._last_adds[-1]
        last_add_record = self.datas[last_add_day][-1]['task']
        self._last_adds.pop()
        self.datas[last_add_day].pop()
        self.save(last_add_day)
        return last_add_record

    def get_recorders(self, day):
        return self.datas[day]

    def get_day_start(self):
        day = self.get_today_day()
        return time.mktime(time.strptime('{} 00:00:00'.format(day), '%Y-%m-%d %H:%M:%S')) + self._day_start

    def record_task(self, name, info):
        day = self.get_today_day()
        recorders = self.get_recorders(self.get_today_day())
        record = {}
        start_time = self.get_day_start()
        if len(recorders):
            start_time = recorders[-1]['end']
        end_time = time.time()
        record['task'] = name
        record['start'] = start_time
        record['end'] = end_time
        record['info'] = info
        self.add_recorder(day, record)
        return record

    def get_task_today_details(self, name):
        records = []
        for record in self.get_recorders(self.get_today_day()):
            if record['task'] == name:
                records.append(record)
        return records


