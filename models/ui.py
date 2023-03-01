from __future__ import annotations
from abc import abstractmethod

import tkinter

class Setting(tkinter.Frame):
    def __init__(self, key:str, displayName:str):
        super().__init__()
        self.key = key
        self.displayName = displayName
        tkinter.Label(self, text=displayName).grid(row=0, column=0)

    @abstractmethod
    def get(self) -> object:
        pass

    @abstractmethod
    def set(self, value:object) -> None:
        pass

class StringSetting(Setting):
    def __init__(self, key: str, displayName: str, initialValue:str=None):
        super().__init__(key, displayName)
        self._var = tkinter.StringVar(value=initialValue)
        tkinter.Entry(self, textvariable=self._var).grid(row=0, column=1)

    def get(self) -> str:
        return self._var.get()

    def set(self, value:str):
        self._var.set(value)

class MultiChoiceSetting(Setting):
    def __init__(self, key: str, displayName:str, initialValueIndex:int=-1, options:list[str]=[]):
        super().__init__(key, displayName)
        self.index = initialValueIndex
        self.options = options

    def get(self) -> str:
        return self.options[self.index]

    def set(self, value:str):
        self.index = self.options.index(value)

class SettingsFrame(tkinter.Frame):
    def __init__(self, master:tkinter.BaseWidget, name:str, settings:list[Setting], *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.name = name
        row = 0
        self._settings = dict[str, object]()
        for setting in settings:
            setting.grid(row=row, column=1)
            row += 1

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
