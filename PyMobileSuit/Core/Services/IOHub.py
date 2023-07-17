from colour import Color
from abc import abstractmethod, ABCMethod
import sys
from datetime import datetime

from PyMobileSuit.IIOHub import IIOHub, IIOHubConfigurator
from PyMobileSuit.ConsoleColor import ConsoleColor
from PyMobileSuit.PrintUnit import PrintUnit

from PyMobileSuit.Core.Services.PromptFormatter import *

class IOHub(IIOHub,ABC):
    """A entity, which serves the input/output of a mobile suit."""

    def __init__(self, promptFormatter: PromptFormatter, configurator: IIOHubConfigurator):
        """Initialize a IOServer."""
        self.ColorSetting = IColorSetting.DefaultColorSetting
        self.Input = sys.stdin
        self.Output = sys.stdout
        self.ErrorStream = sys.stderr
        self.FormatPrompt = promptFormatter
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
        return not sys.stdin is self.Input

    def ResetInput(self) -> None:
        self.Input = sys.stdin

    def ReadLine(self) -> str:
        return self.Input.readline()

    async def ReadLineAsync(self) -> str:
        return await self.Input.readline()

    def Peek(self) -> int:
        raise NotImplementedError()

    def Read(self) -> int:
        return self.Input.read()

    def ReadToEnd(self) -> str:
        return self.Input.read()

    async def ReadToEndAsync(self) -> str:
        return await self.Input.read()

    @property
    def Options(self) -> IOOptions:
        return self._Options

    @Options.setter
    def Options(self, value: IOOptions) -> None:
        self._Options = value

    @property
    def IsErrorRedirected(self) -> bool:
        return not sys.stderr is self.ErrorStream

    @property
    def IsOutputRedirected(self) -> bool:
        return not sys.stdout is self.Output

    @property
    class IOHub(IIOHub):
    # ...

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

    def AppendWriteLinePrefix(self, prefix: PrintUnit) -> None:
        self.Prefix.append(prefix)

    def SubtractWriteLinePrefix(self) -> None:
        self.Prefix.pop()

    def ClearWriteLinePrefix(self) -> None:
        self.Prefix.clear()

    def Write(self, content: PrintUnit) -> None:
        if content.Foreground is not None:
            f = content.Foreground
            self.Output.write(f"\u001b[38;2;{f.R};{f.G};{f.B}m")
        if content.Background is not None:
            b = content.Background
            self.Output.write(f"\u001b[48;2;{b.R};{b.G};{b.B}m")
        self.Output.write(content.Text)
        if content.Foreground is not None or content.Background is not None:
            self.Output.write("\u001b[0m")

    async def WriteAsync(self, content: PrintUnit) -> None:
        if content.Foreground is not None:
            f = content.Foreground
            await self.Output.write(f"\u001b[38;2;{f.R};{f.G};{f.B}m")
        if content.Background is not None:
            b = content.Background
            await self.Output.write(f"\u001b[48;2;{b.R};{b.G};{b.B}m")
        await self.Output.write(content.Text)
        if content.Foreground is not None or content.Background is not None:
            await self.Output.write("\u001b[0m")

    def GetLinePrefix(self, type: OutputType) -> Iterable[PrintUnit]:
        if not IOOptions.DisableLinePrefix in self.Options:
            return self.Prefix
        elif IOOptions.DisableTag in self.Options:
            return []
        else:
            sb = []
            # AppendTimeStamp(sb)
            sb.append(IIOHub.GetLabel(type))
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

    def Write(self, content: Iterable) -> None:
        """Write content to the output stream."""
        self.Output.write(content.Text)

    async def WriteAsync(self, content: Iterable) -> None:
        """Write content to the output stream asynchronously."""
        await self.Output.write(content.Text)

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
            c = Iterable.ConsoleColorCast(cc)
            t = (c.R - r) ** 2 + (c.G - g) ** 2 + (c.B - b) ** 2
            if t == 0:
                return cc
            if t < delta:
                delta = t
                re = cc
        return re

    def Write(self, content: Iterable) -> None:
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

    async def WriteAsync(self, content: Iterable) -> None:
        """Write content to the output stream asynchronously."""
        if content.Foreground is not None:
            f = content.Foreground
            await self.Output.write(f"\u001b[{self.ForegroundCodeOf(f)}m")
        if content.Background is not None:
            b = content.Background
            await self.Output.write(f"\u001b[{self.BackgroundCodeOf(b)}m")
        await self.Output.write(content.Text)
        if content.Foreground is not None or content.Background is not None:
            await self.Output.write("\u001b[0m")

