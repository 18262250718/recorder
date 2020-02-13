import tkinter as tk
from base import BaseActivity


class SettingActivity(BaseActivity):
    def __init__(self, main_activity):
        # 配置值声明
        self.start_time = "00:00:00"
        # 部件声明
        self.text_var = tk.StringVar()
        self.text = None
        # 最后初始化
        super().__init__(main_activity)

    def pack(self, frame):
        self.text = tk.Entry(frame, textvariable=self.text_var)
        self.text.pack()
