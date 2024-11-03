from typing import Optional, Iterable

from colour import Color

from colorama import *

from ..ConsoleColor import ConsoleColor


class PrintUnit:
    """A basic unit of output print, contains foreground, background and text."""

    def __init__(self, Text: str, Foreground: Optional[Color] = None, Background: Optional[Color] = None):
        self.Text = Text
        self.Foreground = Foreground
        self.Background = Background

    @staticmethod
    def ConsoleColorCast(origin: Optional[ConsoleColor]) -> Optional[Color]:
        """Convert ConsoleColor to Color"""
        if origin is None:
            return None
        elif origin == ConsoleColor.DarkYellow:
            return Color("orange")
        else:
            return Color(origin.name.split('.')[-1].lower())

    @classmethod
    def ConsoleColorArrCast(cls, origin: Iterable) -> Iterable:
        """Convert ConsoleColor to Color"""
        def cast(item): return cls.ConsoleColorCast(
            item) if isinstance(item, ConsoleColor) else item
        return map(cast, origin)

    def __iter__(self):
        return iter((self.Text, self.Foreground, self.Background))

    @classmethod
    def FromIterable(cls, tp: Iterable):
        if isinstance(tp, PrintUnit):
            return tp
        return cls(*cls.ConsoleColorArrCast(tp))

    @classmethod
    def FromIterables(cls, tp: Iterable[Iterable]):
        return map(cls.FromIterable, tp)
