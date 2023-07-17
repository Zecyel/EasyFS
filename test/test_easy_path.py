# -*- coding: utf-8 -*-
from .context import easy_fs

EasyPath = easy_fs.easy_path.EasyPath

print('Testing EasyPath.normalize.', end='')

assert EasyPath.normalize('/home/pi/') == '/home/pi'
assert EasyPath.normalize('C:\\Users\\Zecyel\\Desktop') == 'C:/Users/Zecyel/Desktop'
assert EasyPath.normalize('/home/zecyel/./file.txt') == '/home/zecyel/file.txt'
assert EasyPath.normalize('/home/zecyel/../pi/') == '/home/pi'
assert EasyPath.normalize('/home/..') == '/'
assert EasyPath.normalize('/home/./../') == '/'
assert EasyPath.normalize('C:/Users/../') == 'C:/'

print(' Test passed. 7/7')

print('Testing EasyPath.cd.       ', end='')
a = EasyPath('\\home\\pi\\')
assert str(a) == '<EasyPath: /home/pi>'
a.cd('./../')
assert a.path == '/home'
a.cd('./..')
assert a.path == '/'
a.cd('./home/zecyel/')
assert a.path == '/home/zecyel'
a.cd('/python')
assert a.path == '/python'
a.cd('../')
assert a.path == '/'
a.cd('/home')
assert a.path == '/home'

try:
    a.cd('./hello.txt/foo')
except Exception as e:
    assert str(e) == 'Cannot dive into a file.'
assert a.path == '/home'

print(' Test passed. 9/9')

print('Testing EasyPath.sel.       ', end='')

a = EasyPath('/home/pi')
a.sel('foo.txt')
assert a.path == '/home/pi/foo.txt'

try:
    a.sel('bar.foo')
except Exception as e:
    assert str(e) == 'Cannot dive into a file.'

assert a.path == '/home/pi/foo.txt'
a.unsel()
assert a.path == '/home/pi'

a.cd('/')
assert a.path == '/'
a.sel('1.txt')
assert a.path == '/1.txt'

print('Test passed. 5/5')
