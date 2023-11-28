
from ReFreSH.MobileSuit import SuitInfo, Suit, SuitIgnore, SuitAlias, SuitConfig
SuitConfig.LOCALE = 'en'


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

    @SuitInfo("helo")
    def func_with_arg(self, name: str):
        print(f"this is async func {name}")

    @SuitIgnore
    def ignored_func(self):
        print("this is func1")


Suit.QuickStart4BitPowerLine(Hello)
