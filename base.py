import tkinter as tk

class BaseActivity(object):
    def __init__(self, main_activity, onsave=None):
        # 变量
        self._is_run = False
        self._is_open = False
        # 组件
        self.frame_save = None
        self.button_save = None
        self.button_cancel = None
        # 初始化
        self._on_save_func = onsave  # 点击确定之后的回调函数
        from main import MainActivity
        self._main_activity = main_activity  # type:MainActivity
        self._root = self._main_activity.get_root()
        self._top_level = tk.Toplevel()
        self._top_level.resizable(0, 0)
        self._frame = tk.Frame(self._top_level)
        self._top_level.protocol("WM_DELETE_WINDOW", self.on_close)
        self.pack(self._frame)
        self.pack_self(self._frame)
        self._frame.pack()
        self.close()

    def pack(self, frame):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def pack_self(self, frame):
        if not self._on_save_func:
            return
        self.frame_save = tk.Frame(frame)
        self.button_save = tk.Button(self.frame_save, text='确定', command=self.on_click_save)
        self.button_save.grid(row=0, column=0)
        self.button_cancel = tk.Button(self.frame_save, text='取消', command=self.on_close)
        self.button_cancel.grid(row=0, column=1)
        self.frame_save.pack()

    def open(self):
        self._is_open = True
        self._top_level.update()
        self._top_level.deiconify()

    def close(self):
        self._is_open = False
        self._top_level.withdraw()

    def on_close(self):
        self.close()

    def on_click_save(self):
        self.save()
        self._on_save_func()
        self.on_close()

    def is_open(self):
        return self._is_open
