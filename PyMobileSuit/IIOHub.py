from typing import Callable, List, Union, Iterable
from io import TextIOBase
from enum import Flag, auto

from PyMobileSuit.OutputType import OutputType
from PyMobileSuit.Core.ColorSetting import IColorSetting

IIOHubConfigurator = Callable[['IIOHub'], None]

class IOOptions(Flag):
    """Featured Options of IOHub"""
    NoFlag = 0
    """No feature applied."""
    DisablePrompt = auto()
    """Suggests no prompt should be output to the stream"""
    DisableTag = auto()
    """Suggests no type/time tag should be output to the stream"""
    DisableLinePrefix = auto()
    """Suggests no Line prefix should be output to the stream"""

class IIOHub(ABC):
    """A entity, which serves the input/output of a mobile suit."""

    @property
    @abstractmethod
    def Options(self) -> IOOptions:
        """Disable Time marks which shows in Output-Redirected Environment."""
        raise NotImplementedError

    @Options.setter
    @abstractmethod
    def Options(self, value: IOOptions) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def IsErrorRedirected(self) -> bool:
        """Check if this IOServer's error stream is redirected (NOT stderr)"""
        raise NotImplementedError

    @property
    @abstractmethod
    def IsOutputRedirected(self) -> bool:
        """Check if this IOServer's output stream is redirected (NOT stdout)"""
        raise NotImplementedError

    @property
    @abstractmethod
    def ErrorStream(self) -> TextIOBase:
        """Error stream (default stderr)"""
        raise NotImplementedError

    @ErrorStream.setter
    @abstractmethod
    def ErrorStream(self, value: TextIOBase) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def Output(self) -> TextIOBase:
        """Output stream (default stdout)"""
        raise NotImplementedError

    @Output.setter
    @abstractmethod
    def Output(self, value: TextIO) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def ColorSetting(self) -> IColorSetting:
        """Color settings for this IOServer. (default DefaultColorSetting)"""
        raise NotImplementedError

    @ColorSetting.setter
    @abstractmethod
    def ColorSetting(self, value: IColorSetting) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def Input(self) -> TextIO:
        """Input stream (default stdin)"""
        raise NotImplementedError

    @Input.setter
    @abstractmethod
    def Input(self, value: TextIO) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def IsInputRedirected(self) -> bool:
        """Checks if this IOServer's input stream is redirected (NOT stdin)"""
        raise NotImplementedError

    @property
    @abstractmethod
    def FormatPrompt(self) -> PromptFormatter:
        """Prompt server for the io server."""
        raise NotImplementedError

    @staticmethod
    def GetLabel(type: OutputType = OutputType.Default) -> str:
        """get label of given output type"""
        return {
            OutputType.Default: "",
            OutputType.Prompt: "[Prompt]",
            OutputType.Error: "[Error]",
            OutputType.Ok: "[AllOk]",
            OutputType.Title: "[List]",
            OutputType.Info: "[Info]",
            OutputType.System: "[System]"
        }.get(type, "")

    @abstractmethod
    def ResetError(self) -> None:
        """Reset this IOServer's error stream to stderr"""
        raise NotImplementedError

    @abstractmethod
    def ResetOutput(self) -> None:
        """Reset this IOServer's output stream to stdout"""
        raise NotImplementedError

    @abstractmethod
    def AppendWriteLinePrefix(self, prefix: Iterable) -> None:
        """Append a str to Prefix, usually used to increase indentation"""
        raise NotImplementedError

    @abstractmethod
    def SubtractWriteLinePrefix(self) -> None:
        """Subtract a str from Prefix, usually used to decrease indentation"""
        raise NotImplementedError

    @abstractmethod
    def ClearWriteLinePrefix(self) -> None:
        """Clear the prefix before writing line."""
        raise NotImplementedError

    @abstractmethod
    def Write(self, content: Iterable) -> None:
        """Writes some content to output stream, with line break. With certain Input/Output color."""
        raise NotImplementedError

    @abstractmethod
    async def WriteAsync(self, content: Iterable) -> None:
        """Writes some content to output stream asynchronously, with line break. With certain Input/Output color."""
        raise NotImplementedError

    @abstractmethod
    def WriteLine(self, *content: Union[str, Iterable]) -> None:
        """Writes some content to output stream, with line break. With certain Input/Output color."""
        raise NotImplementedError

    @abstractmethod
    async def WriteLineAsync(self, *content: Union[str, Iterable]) -> None:
        """Writes some content to output stream asynchronously, with line break. With certain Input/Output color."""
        raise NotImplementedError

    @abstractmethod
    def ReadLine(self) -> str:
        """Reads a line from input stream"""
        raise NotImplementedError

    @abstractmethod
    async def ReadLineAsync(self) -> str:
        """Reads a line from input stream asynchronously"""
        raise NotImplementedError

    @abstractmethod
    def ReadKey(self, intercept: bool = False) -> ConsoleKeyInfo:
        """Reads a key from input stream"""
        raise NotImplementedError

    @abstractmethod
    async def ReadKeyAsync(self, intercept: bool = False) -> ConsoleKeyInfo:
        """Reads a key from input stream asynchronously"""
        raise NotImplementedError

    @abstractmethod
    def Read(self) -> str:
        """Reads all text from input stream"""
        raise NotImplementedError

    @abstractmethod
    async def ReadAsync(self) -> str:
        """Reads all text from input stream asynchronously"""
        raise NotImplementedError
