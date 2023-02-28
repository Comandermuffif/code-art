from __future__ import annotations

import tkinter

from color_modes import ColorMode
from models import MultiChoiceSetting, Setting, StringSetting

class ColorModeVar(tkinter.Variable):
    def __init__(self, master=None, value:ColorMode=None, name=None):
        super().__init__(master, value, name)
        self.set(value)

    def set(self, value) -> None:
        print(f"Setting {value} with type {type(value)}")
        if value != None and not isinstance(value, ColorMode):
            raise ValueError()
        self.color_mode = value

    def get(self) -> ColorMode:
        print(f"Getting {self.color_mode} with type {type(self.color_mode)}")
        return self.color_mode

class StringSettingFrame(tkinter.Frame):
    def __init__(self, setting:StringSetting, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tkinter.Label(self, text=setting.displayName).grid(row=0, column=0)

        var = tkinter.StringVar(value=setting.get())
        tkinter.Entry(self, textvariable=var).grid(row=0, column=1)

        def _read(a, b, c):
            print("read")
            return setting.get()

        def _write(var, value, mode):
            print("write")
            setting.set(value)

        var.trace_add("read", _read)
        var.trace_add("write", _write)

class MultiChoiceSettingFrame(tkinter.Frame):
    def __init__(self, setting:MultiChoiceSetting, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tkinter.Label(self, text=setting.displayName).grid(row=0, column=0)

        var = tkinter.StringVar(value=setting.get())
        tkinter.OptionMenu(self, var, setting.get(), *setting.options).grid(row=0, column=1)
        # tkinter.Entry(self, textvariable=var).grid(column=1)

        def _read(a, b, c):
            return setting.get()

        def _write(var, value, mode):
            setting.set(value)

        var.trace_add("read", _read)
        var.trace_add("write", _write)

class SettingsFrame(tkinter.Frame):
    def __init__(self, settings:list[Setting], *args, **kwargs):
        super().__init__(*args, **kwargs)

        index = 0
        for setting in settings:
            if type(setting) is StringSetting:
                StringSettingFrame(setting, self).grid(row=index)

            if type(setting) is MultiChoiceSetting:
                MultiChoiceSettingFrame(setting, self).grid(row=index)

            index += 1

