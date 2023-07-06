# -*- coding: utf-8 -*-
from .context import easy_file

EasyPath = easy_file.easy_path.EasyPath

print('Testint EasyPath.normalize. (4)')

assert EasyPath.normalize('/home/pi/') == '/home/pi'
assert EasyPath.normalize('C:\\Users\\Zecyel\\Desktop') == 'C:/Users/Zecyel/Desktop'
assert EasyPath.normalize('/home/zecyel/./file.txt') == '/home/zecyel/file.txt'
assert EasyPath.normalize('/home/zecyel/../pi/') == '/home/pi'

print('Test Passed. 4/4')