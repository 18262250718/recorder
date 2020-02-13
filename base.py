import tkinter as tk


class BaseActivity(object):
    def __init__(self, main_activity):
        from main import MainActivity
        self._main_activity = main_activity # type:MainActivity
        self._root = self._main_activity.get_root()
        self._top_level = tk.Toplevel()
        self._frame = tk.Frame(self._top_level)
        self._is_run = False
        self._is_open = False
        self._top_level.protocol("WM_DELETE_WINDOW", self.on_close)
        self.pack(self._frame)

    def pack(self, frame):
        raise NotImplementedError

    def open(self):
        self._is_open = True
        if self._is_run:
            self._top_level.update()
            self._top_level.deiconify()
        else:
            self._is_run = True
            self._frame.pack()
            self._top_level.mainloop()

    def close(self):
        self._is_open = False
        self._top_level.withdraw()

    def on_close(self):
        self.close()

    def is_open(self):
        return self._is_open
