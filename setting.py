import tkinter as tk
from base import BaseActivity
from config import *


class SettingActivity(BaseActivity):
    def __init__(self, main_activity):
        self.config = main_activity.get_conf()  # type:Config
        # 配置值初始化
        self._day_start = self.config.get_conf(CONF_DAY_START, 0)
        # 部件声明
        self.text_var = tk.StringVar()
        self.text = None
        # 最后初始化
        super().__init__(main_activity)

    def pack(self, frame):
        self.text = tk.Entry(frame, textvariable=self.text_var)
        self.text.pack()
