from typing import Callable, Dict, List, Optional, TypeVar, Iterable

from ..IIOHub import IIOHub
from ..OutputType import OutputType

T = TypeVar('T')


class ConsoleInput:
    """Useful input components for console UI."""

    def __init__(self, io: IIOHub):
        self.hub = io

    @staticmethod
    def ToStringOrEmptySerializer(origin: Optional[T]) -> str:
        """Serialize target with ToString()??""

        Args:
            origin: Origin value

        Returns:
            Serialized target used ToString()??""
        """
        return str(origin) if origin is not None else ""

    def SelectItemFrom(self, prompt: str, selectFrom: List[T],
                          serializer: Optional[Callable[[T], str]] = None,
                          labeler: Optional[Callable[[int, T], str]] = None) -> T:
        """A CUI that allows the user select ONE objective from Alternative objectives.

        Args:
            self
            prompt: Prompt to guide user selection
            selectFrom: Alternative objectives
            serializer: Method of Serializing Object as Text
            labeler: Label of objectives to guide user selection

        Returns:
            Selected item from selectFrom
        """
        serializer = serializer or ConsoleInput.ToStringOrEmptySerializer
        labeler = labeler or (lambda _i, _: str(_i))
        labels = {}
        while True:
            self.hub.WriteLine(prompt, OutputType.Title)
            for i, t in enumerate(selectFrom):
                label = labeler(i, t)
                labels[label] = i
                self.hub.WriteLine([
                    (f"{label}\t", None, self.hub.ColorSetting.TitleColor),
                    (serializer(t), self.hub.ColorSetting.DefaultColor, None)
                ])
            ans = self.hub.ReadLine("", defaultValue="0")
            if ans is not None and ans in labels:
                return selectFrom[labels[ans]]

    class SpaceHyphenParserException(Exception):
        pass

    @classmethod
    def SpaceHyphenParser(cls, userInput: Optional[str], labelMapping: Dict[str, int]) -> Optional[List[int]]:
        """Split user input using space and hyphen. E.g., "1-3 4" will be parsed to {1,2,3,4}.

        Args:
            userInput: String from user
            labelMapping: Dictionary maps label to index.

        Returns:
            Parsed indices or None if failed to parse.
        """
        try:
            return list(ConsoleInput.SpaceHyphenParserInternal(userInput, labelMapping))
        except (cls.SpaceHyphenParserException, KeyError):
            return None

    @classmethod
    def SpaceHyphenParserInternal(cls, userInput: Optional[str], labelMapping: Dict[str, int]) -> Iterable[int]:
        if not userInput:
            return
        inputGroups = userInput.split(' ')
        for inputGroup in inputGroups:
            labels = [labelMapping[l] for l in inputGroup.split("-")]
            if len(labels) == 1:
                yield labels[0]
            elif len(labels) == 2:
                lt, gt = labels
                if gt < lt:
                    raise cls.SpaceHyphenParserException()
                for it in range(lt, gt + 1):
                    yield it
            else:
                raise cls.SpaceHyphenParserException()

    @staticmethod
    def SelectItemsFrom(self, prompt: str, selectFrom: List[T],
                           serializer: Optional[Callable[[T], str]] = None,
                           labeler: Optional[Callable[[int, T], str]] = None,
                           parser: Optional[Callable[[Optional[str], Dict[str, int]], Optional[List[int]]]] = None) -> \
            Iterable[T]:
        """A CUI that allows the user select ONE objective from Alternative objectives.

        Args:
            self
            prompt: Prompt to guide user selection
            selectFrom: Alternative objectives
            serializer: Method of Serializing Object as Text
            labeler: Label of objectives to guide user selection
            parser: Function to parse user input into several int index

        Returns:
            Selected items from selectFrom
        """
        serializer = serializer or ConsoleInput.ToStringOrEmptySerializer
        parser = parser or ConsoleInput.SpaceHyphenParser
        labeler = labeler or (lambda _i, _: str(_i))
        labels = {}
        while True:
            self.hub.WriteLine(prompt, OutputType.Title)
            for i, t in enumerate(selectFrom):
                label = labeler(i, t)
                labels[label] = i
                self.hub.WriteLine([
                    (f"{label}\t", None, self.hub.ColorSetting.TitleColor),
                    (serializer(t), self.hub.ColorSetting.DefaultColor, None)
                ])
            ans = parser(self.hub.ReadLine("", defaultValue="0"), labels)
            if ans is not None:
                return (selectFrom[i] for i in ans)

    @staticmethod
    def SelectYesNo(self, prompt: str, default: Optional[bool] = None) -> bool:
        """A CUI that allows the user answer yes/no by inputting "y" or "n".

        Args:
            self
            prompt: Prompt to guide user input
            default: NULL if only y/n is allowed; Otherwise, if user input is null or empty, such default value will be returned.

        Returns:
            True if user says "yes".
        """
        while True:
            ans = self.hub.ReadLine(prompt)
            if ans is not None:
                ans = ans.lower()
                if ans == "y":
                    return True
                elif ans == "n":
                    return False
                elif not ans and default is not None:
                    return default
