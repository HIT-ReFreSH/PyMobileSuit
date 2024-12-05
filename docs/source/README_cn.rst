
ReFreSH.(Py)MobileSuit
======================

.. image:: https://img.shields.io/pypi/v/PyMobileSuit?style=flat-square
   :target: https://pypi.org/project/PyMobileSuit/
.. image:: https://img.shields.io/github/license/HIT-ReFreSH/PyMobileSuit?style=flat-square
.. image:: https://img.shields.io/github/last-commit/HIT-ReFreSH/PyMobileSuit?style=flat-square
.. image:: https://img.shields.io/github/workflow/status/HIT-ReFreSH/PyMobileSuit/deploy?style=flat-square
.. image:: https://img.shields.io/pypi/format/PyMobileSuit?style=flat-square
.. image:: https://img.shields.io/pypi/wheel/PyMobileSuit?style=flat-square
.. image:: https://img.shields.io/pypi/implementation/PyMobileSuit?style=flat-square
.. image:: https://img.shields.io/github/repo-size/HIT-ReFreSH/PyMobileSuit?style=flat-square
.. image:: https://img.shields.io/github/languages/code-size/HIT-ReFreSH/PyMobileSuit?style=flat-square

`在 PyPI 中查看 <https://pypi.org/project/PyMobileSuit/>`_

MobileSuit 提供了一种快速构建控制台应用程序的简便方法。适用于 Python。

这是 `ReFreSH.MobileSuit <https://github.com/HIT-ReFreSH/MobileSuit>`_ （适用于 .NET）的 Python 版本。

安装
=====

使用以下命令安装：

.. code-block:: shell

   pip install PyMobileSuit

用法
=====

下面是一个简单的例子：

.. code-block:: python

   # Import and Configure
   from ReFreSH.MobileSuit import *

   SuitConfig.LOCALE = 'en'  # 或 'zh'，如果未设置默认为 'en'

   # Write Application Class
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
           print("this is ignored func")

   # Quick Start App
   Suit.QuickStart4BitPowerLine(Hello)
   # 或使用其他快速启动方法:
   # Suit.QuickStart
   # Suit.QuickStartPowerLine

   # 输入 `help` 查看帮助提示。

结果展示
---------

如下图所示为运行结果：

.. image:: ../img/pyms-help.png
   :align: center

导入和配置
===========

使用以下代码即可导入 PyMobileSuit 的全部功能：

.. code-block:: python

   from ReFreSH.MobileSuit import *

PyMobileSuit 有两个主要的配置项：

- ``LOCALE``: 设置语言为 ``en`` 或 ``zh``。
- ``THROW``: 控制是否抛出从应用程序方法捕获的异常。在调试时可以设置为 ``THROW=True``。

编写应用程序类
================

创建您的应用程序类，并使用装饰器定义方法。主要装饰器如下：

- ``@SuitInfo(expr: str, resourceType=None)``:
  - ``expr`` 是方法的描述，会显示在 ``help`` 命令输出中。
  - 如果设置了 ``resourceType``，则 ``getattr(resourceType, expr)`` 将用作描述。
- ``@SuitAlias(alias: str)``: 为方法添加别名。
- ``@SuitIgnore``: 将方法排除为命令。

快速启动应用程序
=================

使用 ``Suit.<QuickStartMethod>(<Your Class>)`` 快速启动应用程序。以下是支持的启动方法：

- ``Suit.QuickStart``: 使用纯文本 IO。
- ``Suit.QuickStartPowerLine``: 支持 True Color Powerline 的 IO。
- ``Suit.QuickStart4BitPowerLine``: 支持 ConsoleColor Powerline 的 IO。

通常建议使用 ``Suit.QuickStart`` 或 ``Suit.QuickStart4BitPowerLine``。

注意事项
========

虽然 MobileSuit 易于使用，但其功能非常全面，目前尚未有完整的文档。

PyMobileSuit 的当前版本是从 C# 项目迁移而来，由 ChatGPT 和手动操作生成，可能存在错误。

