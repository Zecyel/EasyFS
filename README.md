# Easy-File

## Quick Installation

```
pip install easy_file
```

## Warnings

注意！本项目假定所有文件夹的名字中均不含任何特殊字符。（也即，文件夹名只能包含大小写字母、数字和下划线）

例如：`/home/pi`是合法的，而`/etc/init.d/apache2`则被视为非法的。

同时，该项目也支持Windows的路径，能够识别`C:/Users/Zecyel/Desktop`和`C:\Users\Zecyel\Desktop`，但是`C:\Program Files`不能被识别。

## Usage

以下是一个简单示例，详细文档参见[Documentation](./doc/index.md)。



## Testing

在项目根目录下运行如下命令，即可运行所有测试用例。

```
python -m test.all
```
