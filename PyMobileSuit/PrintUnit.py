from colour import Color
from typing import Optional, Tuple

from PyMobileSuit.ConsoleColor import ConsoleColor


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

    def __iter__(self):
        return iter((self.Text, self.Foreground, self.Background))

    @classmethod
    def FromTuple(cls, tp: Tuple[str, Optional[Color], Optional[Color]]):
        return cls(*tp)

    @classmethod
    def FromTriple(cls, tp: Tuple[str, Optional[ConsoleColor], Optional[ConsoleColor]]):
        text, foreground, background = tp
        return cls(*tp)
