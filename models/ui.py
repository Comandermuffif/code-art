from __future__ import annotations
from abc import abstractmethod

import tkinter

from color_modes import ColorMode

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

class Setting(object):
    def __init__(self, key:str, displayName:str):
        self.key = key
        self.displayName = displayName
        self.value = None

    @abstractmethod
    def get(self) -> object:
        return self.value

    @abstractmethod
    def set(self, value:object) -> None:
        self.value = value

class StringSetting(Setting):
    def __init__(self, key: str, displayName: str, initialValue:str=None):
        super().__init__(key, displayName)
        self.value = initialValue

    def get(self) -> str:
        return self.value

    def set(self, value:str):
        self.value = value

class MultiChoiceSetting(Setting):
    def __init__(self, key: str, displayName:str, options:set[str], initialValue:str=None):
        super().__init__(key, displayName)
        self.value = initialValue
        self.options = options

    def get(self) -> str:
        return self.value

    def set(self, value:str):
        self.value = value

class StringSettingFrame(tkinter.Frame):
    def __init__(self, setting:StringSetting, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tkinter.Label(self, text=setting.displayName).grid(column=0)

        var = tkinter.StringVar()
        tkinter.Entry(self, textvariable=var).grid(column=1)

        var.trace_add("r", lambda a, b, c: setting.get())
        var.trace_add("w", lambda a, b, c: setting.set(a))

class MultiChoiceSettingFrame(tkinter.Frame):
    def __init__(self, setting:MultiChoiceSetting, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tkinter.Label(self, text=setting.displayName).grid(column=0)

        var = tkinter.StringVar()
        tkinter.OptionMenu(self, var, setting.value, setting.options)
        tkinter.Entry(self, textvariable=var).grid(column=1)

        var.trace_add("r", lambda a, b, c: setting.get())
        var.trace_add("w", lambda a, b, c: setting.set(a))

class SettingsFrame(tkinter.Frame):
    def __init__(self, settings:list[Setting], *args, **kwargs):
        super().__init__(*args, **kwargs)

        index = 0
        for setting in settings:
            if setting is StringSetting:
                StringSettingFrame(setting, self).grid(row=index)

            if setting is MultiChoiceSetting:
                pass

            index += 1

