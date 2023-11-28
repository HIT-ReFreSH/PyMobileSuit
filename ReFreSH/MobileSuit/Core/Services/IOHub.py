import sys
from abc import ABC
from datetime import datetime
from typing import TextIO, List
from pyasn1.type import char

from ....ConsoleColor import ConsoleColor
from ..ColorSetting import IColorSetting
from .PromptFormatter import *
from ...IIOHub import IIOHub, IIOHubConfigurator, IOOptions
from ...OutputType import OutputType
from ...PrintUnit import PrintUnit


class IOHub(IIOHub, ABC):
    """An entity, which serves the input/output of a mobile suit."""

    def __init__(self, promptFormatter: PromptFormatter, configurator: IIOHubConfigurator):
        """Initialize a IOServer."""
        self._Options: IOOptions = IOOptions.NoFlag
        self.ColorSetting = IColorSetting.DefaultColorSetting()
        self.Input = sys.stdin
        self.Output = sys.stdout
        self.ErrorStream = sys.stderr
        self.FormatPrompt = promptFormatter
        if configurator is not None:
            configurator(self)
        self.Prefix = []

    @property
    def ColorSetting(self) -> IColorSetting:
        return self._ColorSetting

    @ColorSetting.setter
    def ColorSetting(self, value: IColorSetting) -> None:
        self._ColorSetting = value

    @property
    def FormatPrompt(self) -> PromptFormatter:
        return self._FormatPrompt

    @FormatPrompt.setter
    def FormatPrompt(self, value: PromptFormatter) -> None:
        self._FormatPrompt = value

    @property
    def Input(self) -> TextIO:
        return self._Input

    @Input.setter
    def Input(self, value: TextIO) -> None:
        self._Input = value

    @property
    def IsInputRedirected(self) -> bool:
        return sys.stdin is not self.Input

    def ResetInput(self) -> None:
        self.Input = sys.stdin

    def ReadLinePrimary(self) -> str:
        return self.Input.readline()

    def Peek(self) -> char:
        next_char = self.Input.read(1)
        self.Input.seek(self.Input.tell() - 1)
        return next_char

    def Read(self) -> char:
        return self.Input.read(1)

    def ReadToEnd(self) -> str:
        return '\n'.join(self.Input.readlines())

    @property
    def Options(self) -> IOOptions:
        return self._Options

    @Options.setter
    def Options(self, value: IOOptions) -> None:
        self._Options = value

    @property
    def IsErrorRedirected(self) -> bool:
        return sys.stderr is not self.ErrorStream

    @property
    def IsOutputRedirected(self) -> bool:
        return sys.stdout is not self.Output

    @property
    def ErrorStream(self) -> TextIO:
        return self._ErrorStream

    @ErrorStream.setter
    def ErrorStream(self, value: TextIO) -> None:
        self._ErrorStream = value

    @property
    def Output(self) -> TextIO:
        return self._Output

    @Output.setter
    def Output(self, value: TextIO) -> None:
        self._Output = value

    def ResetError(self) -> None:
        self.ErrorStream = sys.stderr

    def ResetOutput(self) -> None:
        self.Output = sys.stdout

    def AppendWriteLinePrefixPrimary(self, prefix: Iterable) -> None:
        self.AppendWriteLinePrefixInternal(PrintUnit.FromIterable(prefix))

    def AppendWriteLinePrefixInternal(self, prefix: PrintUnit) -> None:
        self.Prefix.append(prefix)

    def SubtractWriteLinePrefix(self) -> None:
        self.Prefix.pop()

    def ClearWriteLinePrefix(self) -> None:
        self.Prefix.clear()

    def WritePrimary(self, content: Iterable) -> None:
        self.WriteInternal(PrintUnit.FromIterable(content))

    def WriteInternal(self, content: PrintUnit) -> None:

        if content.Foreground is not None:
            (R, G, B) = content.Foreground.rgb
            self.Output.write(f"\u001b[38;2;{R};{G};{B}m")
        if content.Background is not None:
            (R, G, B) = content.Background
            self.Output.write(f"\u001b[48;2;{R};{G};{B}m")
        self.Output.write(content.Text)
        if content.Foreground is not None or content.Background is not None:
            self.Output.write("\u001b[0m")

    def GetLinePrefix(self, otype: OutputType) -> List[PrintUnit]:
        if IOOptions.DisableLinePrefix not in self.Options:
            return self.Prefix
        elif IOOptions.DisableTag in self.Options:
            return []
        else:
            sb = [IIOHub.GetLabel(otype)]
            # AppendTimeStamp(sb)
            return [PrintUnit(''.join(sb), None)]

    @staticmethod
    def AppendTimeStamp(sb: List[str]) -> None:
        sb.append('[')
        sb.append(datetime.now().isoformat())
        sb.append(']')


class PureTextIOHub(IOHub):
    """IO hub with pure text output."""

    def __init__(self, promptFormatter: PromptFormatter, configurator: IIOHubConfigurator):
        """Initialize a IOhub."""
        super().__init__(promptFormatter, configurator)

    def WritePrimary(self, content: Iterable) -> None:
        """Write content to the output stream."""
        self.Output.write(PrintUnit.FromIterable(content).Text)


class IOHub4Bit(IOHub):
    """IO hub using 4-bit color output."""

    def __init__(self, promptFormatter: PromptFormatter, configurator: IIOHubConfigurator):
        """Initialize a IOhub."""
        super().__init__(promptFormatter, configurator)

    @staticmethod
    def BackgroundCodeOf(c: Color) -> int:
        return 10 + IOHub4Bit.ForegroundCodeOf(c)

    @staticmethod
    def ForegroundCodeOf(c: Color) -> int:
        return {
            ConsoleColor.Black: 30,
            ConsoleColor.DarkBlue: 34,
            ConsoleColor.DarkGreen: 32,
            ConsoleColor.DarkCyan: 36,
            ConsoleColor.DarkRed: 31,
            ConsoleColor.DarkMagenta: 35,
            ConsoleColor.DarkYellow: 33,
            ConsoleColor.Gray: 90,
            ConsoleColor.DarkGray: 37,
            ConsoleColor.Blue: 94,
            ConsoleColor.Green: 92,
            ConsoleColor.Cyan: 96,
            ConsoleColor.Red: 91,
            ConsoleColor.Magenta: 95,
            ConsoleColor.Yellow: 93,
            ConsoleColor.White: 97
        }[IOHub4Bit.ConsoleColorOf(c)]

    @staticmethod
    def ConsoleColorOf(color: Color) -> ConsoleColor:

        (r, g, b) = color.rgb
        delta = float("inf")
        re = None
        for cc in ConsoleColor:
            c = PrintUnit.ConsoleColorCast(cc)
            (cr,cg,cb) =c.rgb
            t = (cr - r) ** 2 + (cg - g) ** 2 + (cb - b) ** 2
            if t == 0:
                return cc
            if t < delta:
                delta = t
                re = cc
        return re

    def WriteInternal(self, content: PrintUnit) -> None:
        """Write content to the output stream."""
        if content.Foreground is not None:
            f = content.Foreground
            self.Output.write(f"\u001b[{self.ForegroundCodeOf(f)}m")
        if content.Background is not None:
            b = content.Background
            self.Output.write(f"\u001b[{self.BackgroundCodeOf(b)}m")
        self.Output.write(content.Text)
        if content.Foreground is not None or content.Background is not None:
            self.Output.write("\u001b[0m")
