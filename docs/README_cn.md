<div  align=center>
    <img src="https://raw.githubusercontent.com/HIT-ReFreSH/PyMobileSuit/main/images/logo.png" width = 30% height = 30%  />
</div>

# ReFreSH.(Py)MobileSuit

![PyPI](https://img.shields.io/pypi/v/PyMobileSuit?style=flat-square)
![GitHub](https://img.shields.io/github/license/HIT-ReFreSH/PyMobileSuit?style=flat-square)
![GitHub last commit](https://img.shields.io/github/last-commit/HIT-ReFreSH/PyMobileSuit?style=flat-square)
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/HIT-ReFreSH/PyMobileSuit/deploy?style=flat-square)
![PyPI - Format](https://img.shields.io/pypi/format/PyMobileSuit?style=flat-square)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/PyMobileSuit?style=flat-square)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/PyMobileSuit?style=flat-square)
![GitHub repo size](https://img.shields.io/github/repo-size/HIT-ReFreSH/PyMobileSuit?style=flat-square)
![GitHub code size](https://img.shields.io/github/languages/code-size/HIT-ReFreSH/PyMobileSuit?style=flat-square)

[在PyPI中查看](https://pypi.org/project/PyMobileSuit/)

MobileSuit 提供了一种快速构建控制台应用程序的简便方法。适用于 Python。

> 这是 [ReFreSH.MobileSuit](https://github.com/HIT-ReFreSH/MobileSuit)（适用于.NET）的 Python 版本。

## 安装

```
pip install PyMobileSuit
```

## 用法

下面是一个简单的例子：

```python
# [Import and Configure]
from src.ReFreSH import *

SuitConfig.LOCALE = 'en'  # 'zh' or 'en' (default if not set)


# [Write Application Class]
class Hello(object):
    def __init__(self):
        pass

    @SuitInfo("hello")
    def instance_func(self):
        print("this is instance function")

    @SuitInfo("async")
    @SuitAlias("async")
    async def async_func(self):
        print("this is async func")

    @SuitInfo("helo <name>")
    @SuitAlias("helo")
    def func_with_arg(self, name: str):
        print(f"this is async func {name}")

    @SuitInfo("helos <names>[]")
    @SuitAlias("helos")
    def func_with_list_arg(self, names: list[str]):
        print(f"this is async func {','.join(names)}")

    @SuitIgnore
    def ignored_func(self):
        print("this is func1")


# [Quick Start App]
Suit.QuickStart4BitPowerLine(Hello)
# Suit.QuickStart
# Suit.QuickStartPowerLine

# > type `help` after the prompt.
```

下图为结果：

<div  align=center>
    <img src="../img/pyms-help.png"/>
</div>
### 导入和配置

`from ReFreSH.MobileSuit import SuitInfo, Suit, SuitIgnore, SuitAlias, SuitConfig `是通常所需的全部内容。

 对于 PyMobileSuit，有两个配置项：

- LOCALE: 设置语言为 `en` 或 `zh`。

- THROW: 用于确定是否应抛出从应用程序方法捕获的异常。要调试应用程序，您可能需要设置`THROW=True`。

### 编写应用程序类

创建您的应用程序类，编写具有或不具有参数的普通或异步方法。有三个基本的装饰器可用于应用程序方法：

- `@SuitInfo(expr: str, resourceType=None)`: `expr` 是默认情况下显示在 `help`命令输出中的描述。如果您还设置了 `resourceType`，那么 `getattr(resourceType, expr)` 将是描述。
- `@SuitAlias(alias: str)`: 为方法添加除了方法名称的别名。
- `@SuitIgnore`: 假设该方法不是一个命令。

### 快速启动应用程序

使用 `Suit.<QuickStartMethod>(<Your Class>) `快速启动应用程序。有三个内置的 `QuickStartMethod` 可以实现：

- Suit.QuickStart: 不带 Powerline 的纯文本 IO。

- Suit.QuickStartPowerLine: 支持 True color Powerline 的 IO。

- Suit.QuickStart4BitPowerLine: 支持 ConsoleColor Powerline 的 IO。

通常，您应该使用 `Suit.QuickStart` 或 `Suit.QuickStart4BitPowerLine`。 

## 注意

尽管 MobileSuit 很容易使用，但其功能非常全面，所以我还没有时间编写完整的文档。

PyMobileSuit 的当前版本是从 C# 迁移而来，使用了 ChatGPT 和手动操作，而不是重新编写，因此可能存在错误。
 