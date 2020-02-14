import tkinter as tk
from config import *
from recorder import Recorder


class BaseFrame(object):
    def __init__(self, main_activity):
        self._main_activity = main_activity  # type:MainActivity
        self._root = self._main_activity.get_root()
        self._conf = self._main_activity.get_conf()     # type:Config
        self._recorder = self._main_activity.get_recorder() # type:Recorder
        self._frame = tk.Frame(self._root)
        self.pack(self._frame)
        self.init_activities()

    def pack(self, frame):
        raise NotImplementedError

    def init_activities(self):
        raise NotImplementedError

    # 窗口管理类接口
    def show(self, row, col):
        self._frame.grid(row=row, column=col)

    def close(self):
        self._frame.grid_forget()


class TaskFrame(BaseFrame):
    def __init__(self, main_activity, task_name, task_details=[]):
        # 变量
        self._task_name = task_name
        self._task_details = task_details   # [ {'start':, 'end':, 'info':}  ]
        self._tmp_info = ''
        self._last_infos = []  # 用于撤销
        # 组件
        self.label_name = None
        self.button_record = None
        self.button_del = None
        self.button_info = None
        self.button_insert = None
        self.label_time = None
        # 组件变量
        self.label_time_text = tk.StringVar()
        # 窗口
        self.activity_info = None
        # 初始化
        super(TaskFrame, self).__init__(main_activity)

    # 继承接口
    def pack(self, frame):
        self.label_name = tk.Label(frame, text=self._task_name)
        self.label_name.grid(row=0, column=0)
        self.button_record = tk.Button(frame, text='记录', command=self.on_click_record)
        self.button_record.grid(row=0, column=1)
        self.button_del = tk.Button(frame, text='删除', command=self.on_click_del)
        self.button_del.grid(row=0, column=2)
        self.button_info = tk.Button(frame, text='备注', command=self.on_click_info)
        self.button_info.grid(row=0, column=3)
        self.button_insert = tk.Button(frame, text='插入', command=self.on_click_insert)
        self.button_insert.grid(row=0, column=4)
        self.label_time = tk.Label(frame, textvariable=self.label_time_text)
        self.label_time.grid(row=0, column=5)
        self.label_time_text.set('{:.2f}h'.format(self.get_all_time() / 3600))

    def init_activities(self):
        from info import InfoActivity
        self.activity_info = InfoActivity(self._main_activity, self.on_save_info)
        pass

    # 外部接口
    def get_name(self):
        return self._task_name

    def get_last_info(self):
        if len(self._task_details):
            return None
        else:
            return self._task_details[-1]["info"]

    def get_all_time(self):
        all_time = 0
        for info in self._task_details.__iter__():
            all_time += ( info['end'] - info['start'] )
        return all_time

    def update(self):
        self._task_details = self._recorder.get_task_today_details(self._task_name)
        self.label_time_text.set('{:0.2f}h'.format(self.get_all_time()/3600))

    def cancel_last(self):
        self.update()
        if len(self._last_infos):
            self.activity_info.set_text(self._last_infos[-1])
            self._last_infos.pop()

    # 功能类接口
    def on_click_record(self):
        self._recorder.record_task(self._task_name, self.activity_info.get_text())
        self.label_time_text.set('{:.2f}h'.format(self.get_all_time()/3600))
        # 清空记录
        self._last_infos.append(self.activity_info.get_text())
        self.activity_info.clear()
        self.update()

    def on_click_del(self):
        self._main_activity.del_task(self)

    def on_click_info(self):
        self.activity_info.open()

    def on_click_insert(self):
        pass

    def on_save_info(self):
        pass


class HeadFrame(BaseFrame):
    def __init__(self, main_activity):
        # 变量
        # 组件声明
        self.entry_task = None
        self.button_add = None
        self.button_cancel = None
        self.button_history = None
        self.button_set = None
        # 组件变量
        self.entry_task_text = tk.StringVar()
        # 窗口
        self.activity_history = None
        self.activity_setting = None
        # 初始化
        super(HeadFrame, self).__init__(main_activity)

    def pack(self, frame):
        self.entry_task = tk.Entry(frame, textvariable=self.entry_task_text)
        self.entry_task.grid(row=0, column=0)
        self.button_add = tk.Button(frame, text='添加', command=self.on_click_add)
        self.button_add.grid(row=0, column=1)
        self.button_cancel = tk.Button(frame, text='撤销', command=self.on_click_cancel)
        self.button_cancel.grid(row=0, column=2)
        self.button_history = tk.Button(frame, text='历史', command=self.on_click_history)
        self.button_history.grid(row=0, column=3)
        self.button_set = tk.Button(frame, text='设置', command=self.on_click_setting)
        self.button_set.grid(row=0, column=4)

    def init_activities(self):
        from history import HistoryActivity
        self.activity_history = HistoryActivity(self._main_activity)
        from setting import SettingActivity
        self.activity_setting = SettingActivity(self._main_activity)

    def on_click_add(self):
        name = self.entry_task_text.get()
        self._main_activity.add_task(name)

    def on_click_cancel(self):
        self._main_activity.cancel_record()
        pass

    def on_click_history(self):
        pass

    def on_click_setting(self):
        pass

    def on_save_setting(self):

        pass


class MainActivity(object):
    def __init__(self):
        # 初始化
        self.root = tk.Tk()
        self.root.title('记录器')
        self.root.resizable(0, 0)
        # 配置
        self.config = None
        self.task_recorder = None
        self.load_config()
        # 变量
        self.head_frame = None
        self.task_frames = {}
        # 根据配置初始化
        self.init_by_config()

    def open(self):
        self.head_frame = HeadFrame(self)
        self.head_frame.show(0, 0)
        self.root.mainloop()

    def load_config(self):
        self.config = Config('config.json')
        self.task_recorder = Recorder(self.config)

    def init_by_config(self):
        # 根据配置添加任务
        tasks = self.config.get_conf(CONF_TASKS, []) # type:list
        for taskname in tasks.__iter__():
            self.add_task(taskname, False)

    def get_root(self):
        return self.root

    def get_conf(self):
        return self.config

    def add_task(self, name, save=True):
        if len(name) == 0 or name in self.task_frames:
            return
        task_frame = TaskFrame(self, name, self.task_recorder.get_task_today_details(name))
        self.task_frames[name] = task_frame
        task_frame.show(len(self.task_frames), 0)
        # 添加进配置
        if save:
            conf_tasks = self.config.get_conf(CONF_TASKS, []) # type:list
            conf_tasks.append(name)
            self.config.save_conf(CONF_TASKS, conf_tasks)

    def get_recorder(self):
        return self.task_recorder

    def del_task(self, task):
        assert isinstance(task, TaskFrame)
        name = task.get_name()
        if name not in self.task_frames or task is not self.task_frames[name]:
            return
        self.task_frames.pop(name)
        task.close()
        # 添加进配置
        conf_tasks = self.config.get_conf(CONF_TASKS, []) # type:list
        conf_tasks.remove(name)
        self.config.save_conf(CONF_TASKS, conf_tasks)

    def update_task(self, name, cancel=False):
        if name not in self.task_frames:
            return
        if cancel:
            self.task_frames[name].cancel_last()
        else:
            self.task_frames[name].update()

    def cancel_record(self):
        record = self.task_recorder.cancel_record()
        self.update_task(record, cancel=True)


if __name__ == '__main__':
    root = MainActivity()
    root.open()
