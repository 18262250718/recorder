import tkinter as tk


class MainActivity(object):
    def __init__(self):
        # 变量
        # 组件声明
        self.button = None
        # 界面声明
        self.setting = None
        # 初始化
        self.root = tk.Tk()
        self.pack(self.root)
        pass

    def pack(self, root):
        self.button = tk.Button(root, command=self.on_click)
        self.button.pack()
        pass

    def on_click(self):
        from setting import SettingActivity
        if self.setting is None:
            self.setting = SettingActivity(self)
        if not self.setting.is_open():
            self.setting.open()
        else:
            self.setting.close()

    def open(self):
        self.root.mainloop()

    def get_root(self):
        return self.root


if __name__ == '__main__':
    root = MainActivity()


    root.open()