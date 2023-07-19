from typing import Callable, Iterable

from colour import Color

from ...PrintUnit import PrintUnit
from ...Resources import Lang

PromptFormatter = Callable[[Iterable[PrintUnit]], Iterable[PrintUnit]]
"""
represents a generator provides prompt output.
"""


class PromptFormatters:
    """Default prompt formatters."""

    Lightning = '\u26A1'
    """a lightning ⚡ char"""

    RightArrow = ''
    """a right arrow  char"""

    RightTriangle = ''
    """a right triangle  char"""

    Cross = '⨯'
    """a cross ⨯ char"""

    @staticmethod
    def BasicPromptFormatter(origin: Iterable[PrintUnit]) -> Iterable[PrintUnit]:
        """A basic prompt formatter for Mobile Suit."""
        l = []
        orgList = list(origin)
        for i, unit in enumerate(orgList):
            output = []
            if i == 0:
                output.append(' ')
            output.append(f"[{unit.Text}] ")
            if i == len(orgList) - 1:
                output.append('>')
            l.append(PrintUnit(''.join(output), unit.Foreground, unit.Background))
        return l

    @staticmethod
    def PowerLineFormatter(origin: Iterable[PrintUnit]) -> Iterable[PrintUnit]:
        """A PowerLine themed prompt generator"""
        orgList = list(origin)
        # Power line theme uses inverse Background&Foreground
        backGrounds = [p.Foreground or Color.Black for p in orgList]
        foreGrounds = [p.Background for p in orgList]
        for i in range(len(orgList)):
            if foreGrounds[i] is not None:
                continue
            bg = backGrounds[i]
            foreGrounds[i] = Color.White if bg.R <= 0x7F or bg.G <= 0x7F or bg.B <= 0x7F else Color.Black

        r = []
        if len(orgList) > 0:
            r.append(PrintUnit(" ", foreGrounds[0], backGrounds[0]))
        for i in range(len(orgList)):
            txt = orgList[i].Text
            if txt.startswith(Lang.Tasks):
                txt = txt.replace(Lang.Tasks, f"{PromptFormatters.Lightning} ", 1)
            r.append(PrintUnit(f"{txt}", foreGrounds[i], backGrounds[i]))
            r.append(PrintUnit(" ", foreGrounds[i], backGrounds[i]))
            r.append(PrintUnit(f"{PromptFormatters.RightTriangle} ", backGrounds[i], backGrounds[i + 1] if i + 1 < len(orgList) else None))
        return r
