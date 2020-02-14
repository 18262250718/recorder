import tkinter as tk
from base import BaseActivity


class InfoActivity(BaseActivity):
    def __init__(self, main_activity, onsave):
        # 配置值声明
        # 部件声明
        self.text_var = tk.StringVar()
        self.text = None
        # 最后初始化
        super().__init__(main_activity, onsave)

    def pack(self, frame):
        self.text = tk.Text(frame)
        self.text.pack()

    def clear(self):
        assert isinstance(self.text, tk.Text)
        self.text.delete('0.0', 'end')

    def save(self):
        pass

    def get_text(self):
        return self.text.get('0.0', 'end')

    def set_text(self, text):
        assert isinstance(self.text, tk.Text)
        self.clear()
        self.text.insert(tk.INSERT, text)
        print('ee')