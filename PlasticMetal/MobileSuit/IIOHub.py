from abc import ABC, abstractmethod
from enum import Flag, auto
from io import TextIOBase
from typing import Callable, Union, Iterable, Optional, List

from colour import Color
from pyasn1.type import char

from PlasticMetal.ConsoleColor import ConsoleColor
from .Core.ColorSetting import IColorSetting
from .Core.Services.PromptFormatter import PromptFormatter
from .OutputType import OutputType
from .PrintUnit import PrintUnit

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
    """An entity, which serves the input/output of a mobile suit."""

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
    def Output(self, value: TextIOBase) -> None:

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
    def Input(self) -> TextIOBase:
        """Input stream (default stdin)"""

        raise NotImplementedError

    @Input.setter
    @abstractmethod
    def Input(self, value: TextIOBase) -> None:

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
    def GetLabel(otype: OutputType = OutputType.Default) -> str:
        """get label of given output type"""

        return {

            OutputType.Default: "",

            OutputType.Prompt: "[Prompt]",

            OutputType.Error: "[Error]",

            OutputType.Ok: "[AllOk]",

            OutputType.Title: "[List]",

            OutputType.Info: "[Info]",

            OutputType.System: "[System]"

        }.get(otype, "")

    @abstractmethod
    def ResetError(self) -> None:
        """Reset this IOServer's error stream to stderr"""

        raise NotImplementedError

    @abstractmethod
    def ResetOutput(self) -> None:
        """Reset this IOServer's output stream to stdout"""

        raise NotImplementedError

    @abstractmethod
    def AppendWriteLinePrefixPrimary(self, prefix: Iterable) -> None:
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
    def WritePrimary(self, content: Iterable) -> None:
        """Writes some content to output stream, with line break. With certain Input/Output color."""

        raise NotImplementedError

    @abstractmethod
    def GetLinePrefix(self, otype: OutputType) -> List[Iterable]:
        """Get the prefix before writing line."""

        raise NotImplementedError

    @abstractmethod
    def ResetInput(self) -> None:
        """Reset this IOServer's input stream to stdin"""

        raise NotImplementedError

    @abstractmethod
    def ReadLinePrimary(self) -> Optional[str]:
        """Reads a line from input stream, with prompt.


        Returns:

            Content from input stream, None if EOF
        """

        raise NotImplementedError

    @abstractmethod
    def Peek(self) -> char:
        """Reads the next character from input stream without changing the state of the reader or the character source.


        Returns:

            The next available character.
        """

        raise NotImplementedError

    @abstractmethod
    def Read(self) -> char:
        """Reads the next character from input stream.


        Returns:

            The next available character.
        """

        raise NotImplementedError

    @abstractmethod
    def ReadToEnd(self) -> str:
        """Reads all characters from the current position to the end of the input stream and returns them as one string.


        Returns:

            All characters from the current position to the end.
        """

        raise NotImplementedError

    def AppendWriteLinePrefix(self, prefix: Union[str, Iterable] = "\t") -> None:
        """Append a str to Prefix, usually used to increase indentation

        Args:
            self: IOHub to write to
            prefix: the output tuple to append
        """
        if isinstance(prefix, str):
            prefix = (prefix, None, None)
        self.AppendWriteLinePrefixPrimary(prefix)

    def Write(self, content: Union[str, Iterable[Iterable]], otype: OutputType = OutputType.Default,
              custom_color: Optional[Union[ConsoleColor, Color]] = None) -> None:
        """Writes some content to output stream. With certain color in console.

        Args:
            content: Content to output.
            otype: Optional. Type of this content, this decides how will it be like.
            custom_color: Optional. Customized color in console
        """
        content = self._StrToPrintUnit(content, custom_color, otype)
        content = PrintUnit.FromIterables(content)
        if otype == OutputType.Prompt:
            if self.IsOutputRedirected:
                return
            content = self.FormatPrompt(content)

        for unit in content:
            self.WritePrimary(unit)

    def _StrToPrintUnit(self, content, custom_color, otype):
        if isinstance(content, str):
            if isinstance(custom_color, ConsoleColor):
                custom_color = PrintUnit.ConsoleColorCast(custom_color)
            sel_color = IColorSetting.SelectColor(
                self.ColorSetting, otype, custom_color)
            if otype == OutputType.Prompt:
                if not self.IsOutputRedirected:
                    content = self.FormatPrompt(
                        [PrintUnit.FromIterable((content, sel_color))])
            else:
                content = [(content, sel_color, None)]
        return content

    def WriteLine(self, content: Union[str, Iterable[Iterable]] = "", otype: OutputType = OutputType.Default,
                  custom_color: Optional[Union[ConsoleColor, Color]] = None) -> None:
        """Writes some content to output stream, with line break. With certain color in console.

        Args:

            content: Content to output.
            otype: Optional. Type of this content, this decides how will it be like.
            custom_color: Optional. Customized color in console
        """
        content = self._StrToPrintUnit(content, custom_color, otype)

        self.Write(self.GetLinePrefix(otype) + content + [("\n", None)], otype)

    def ReadLine(self, prompt: str = '', newLine: bool = False, customPromptColor: Optional[Color] = None,
                 defaultValue: Optional[str] = None) -> Optional[str]:
        """Reads a line from input stream, with prompt. Return something default if user input "".

        Args:
            prompt: The prompt display(output to output stream) before user input.
            newLine: If the prompt will display in a single line
            customPromptColor: Optional. Prompt's Color, ColorSetting.PromptColor as default.
            defaultValue: Default return value if user input ""

        Returns:
            Content from input stream, None if EOF, if user input "", return defaultValue
        """
        if len(prompt) > 0:
            self.Write(self.CreateReadLinePrompt(prompt, defaultValue, customPromptColor), OutputType.Prompt)
        if newLine:
            self.Write("\n")

        r = self.ReadLinePrimary()
        if r is None:
            return None

        stringBuilder = r
        while len(stringBuilder) > 1 and stringBuilder[-2:] == ' %':
            stringBuilder = stringBuilder[:-2]
            r = self.ReadLinePrimary()
            if r is None:
                break
            stringBuilder += r

        return defaultValue if len(stringBuilder) == 0 else stringBuilder

    def CreateReadLinePrompt(self, prompt: str, defaultValue: Optional[str], customPromptColor: Optional[Color]) -> \
            Iterable[Iterable]:
        printUnit0 = (
            prompt, customPromptColor or self.ColorSetting.PromptColor)
        return [printUnit0] if defaultValue is None else [printUnit0, (defaultValue, self.ColorSetting.SystemColor)]
