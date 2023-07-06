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

    # Member Definitions
    # path: str

    # Magic Methods    
    def __init__(self, path = None) -> None:
        self.path = EasyPath.standardization(path)

    def __str__(self) -> str:
        return f'<EasyPath: {self.path}>'

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name == 'path':
            super().__setattr__(__name, EasyPath.standardization(__value))

    # Static Methods
    @staticmethod
    def standardization(path: str) -> str:
        path = path.replace('\\', '/')  # shift Windows-style path to Unix-style
        if path[-1] == '/':
            path = path[:-1]    # for eg., "/etc/apt/" should be written as "/etc/apt"
        if path.find('.') != -1 and path.index('.') < path.rindex('/'):
            raise Exception("Cannot dive into a file.") # you should never write "/etc/apt/sources.list/foo"
                                                        # "init.d/" is not to be considered.
        return path

    @staticmethod
    def join(base: str, rel: str) -> str:   # It's different to os.path.join()
        base = EasyPath.standardization(base)
        rel = EasyPath.standardization(rel)
        if rel[0] == '/':
            merge = base[:base.index('/')] + rel    # for eg. "C:/Pictures" and "/videos" merges to "C:/videos"
                                                    # "/home/etc" and "/dev/null" merges to "/dev/null"
        else:
            merge = f"{base}/{rel}"

        # simplify '../' and './'
        merge += '/'
        while '../' in merge:
            indx = merge.index('../')
            lindx = merge.rindex('/', 0, indx - 1)
            merge = merge[:lindx] + merge[indx + 3:]
        merge.replace('./', '')

        merge = EasyPath.standardization(merge)
        if merge == '':
            merge = '/'
        return merge

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
        return self.cd('../')

