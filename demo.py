from PyMobileSuit.Decorators import *
import inspect
import PyMobileSuit.Decorators.DecoratorUtils as DecoratorUtils

class Test(object):
    def __init__(self):
        pass
    @SuitInfo(".gitignore")
    @SuitAlias(".gitignor2")
    @SuitAlias(".githh")
    def instance_func(self):
        print("this is func1")

    @SuitIgnore
    def ignored_func(self):
        print("this is func1")

methods=inspect.getmembers(Test,lambda m: inspect.isfunction(m) and not DecoratorUtils.is_ignored(m))
for method_name,method in methods:
    print(DecoratorUtils.get_alias(method))
    print(DecoratorUtils.get_info(method))