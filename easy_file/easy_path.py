# -*- coding: utf-8 -*-
import os
from typing import Any, List, TypedDict
from enum import Enum

class ItemType(Enum):
    DUMMY = 0
    FILE = 1
    FOLDER = 2

class PropertyDict(TypedDict):
    type: ItemType
    name: str
    path: 'EasyPath'
    size: int           # Only File

class EasyPath:

    # Magic Methods    
    def __init__(self, path = None) -> None:
        self.path = EasyPath.normalize(path)

    def __str__(self) -> str:
        return f'<EasyPath: {self.path}>'

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'path':
            super().__setattr__(__name, EasyPath.normalize(__value))

    # Static Methods
    @staticmethod
    def normalize(path: str) -> str:
        path = path.replace('\\', '/')  # shift Windows-style path to Unix-style
        if path[-1] == '/':
            path = path[:-1]    # for eg., "/etc/apt/" should be written as "/etc/apt"
        
        # simplify '../' and './'
        path += '/'
        path = path.replace('/./', '/')

        while '../' in path:
            indx = path.index('../')
            lindx = path.rindex('/', 0, indx - 1)
            path = path[:lindx + 1] + path[indx + 3:]
        if path[-1] == '/':
            path = path[:-1]
        if path == '' or path[-1] == ':':   # add a slash for "C:/apple/.." and "/home/.."
            path += '/'

        if path.find('.') != -1 and path.index('.') < path.rindex('/'):
            raise Exception("Cannot dive into a file.") # you should never write "/etc/apt/sources.list/foo"
                                                        # "init.d/" is not to be considered.
        return path

    @staticmethod
    def join(base: str, rel: str) -> str:   # It's different to os.path.join()
        base = EasyPath.normalize(base)
        if rel[0] in '/\\':
            merge = base[:base.index('/')] + rel    # for eg. "C:/Pictures" and "/videos" merges to "C:/videos"
                                                    # "/home/etc" and "/dev/null" merges to "/dev/null"
        else:
            if base[-1] == '/': # "/" and "C:/" and etc.
                merge = base + rel
            else:
                merge = f"{base}/{rel}"

        return EasyPath.normalize(merge)

    @staticmethod
    def cwd() -> 'EasyPath':
        return EasyPath(os.getcwd())

    # Private Methods
    def __join(self, path: str) -> 'EasyPath':
        self.path = EasyPath.join(self.path, path)
        return self

    # Public Methods
    def cd(self, rel: str) -> 'EasyPath':
        return self.__join(rel)

    def ls(self) -> List[PropertyDict]:
        lst = os.listdir(self.path)
        ret = []
        for item in lst:
            dic: PropertyDict = {'name': item}
            path = os.path.join(self.path, item)
            dic['path'] = EasyPath(path)
            if os.path.isfile(path):
                dic['type'] = ItemType.FILE
                dic['size'] = os.path.getsize(path)
            elif os.path.isdir(path):
                dic['type'] = ItemType.FOLDER
            else:
                dic['type'] = ItemType.DUMMY
            ret.append(dic)
        return ret
    
    def sel(self, filename: str) -> 'EasyPath':
        return self.cd(filename)
    
    def unsel(self) -> 'EasyPath':
        return self.cd('..')
