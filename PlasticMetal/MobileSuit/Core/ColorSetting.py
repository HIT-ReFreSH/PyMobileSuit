from abc import ABC, abstractmethod
from typing import Optional

from colour import Color

from ..OutputType import OutputType


class IColorSetting(ABC):
    """Color settings of a Mobile Suit."""

    @property
    @abstractmethod
    def BackgroundColor(self) -> Color:
        """BackgroundColor"""
        raise NotImplementedError

    @BackgroundColor.setter
    @abstractmethod
    def BackgroundColor(self, value: Color) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def DefaultColor(self) -> Color:
        """Default color. For OutputType.Default"""
        raise NotImplementedError

    @DefaultColor.setter
    @abstractmethod
    def DefaultColor(self, value: Color) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def PromptColor(self) -> Color:
        """Prompt Color. For OutputType.Prompt"""
        raise NotImplementedError

    @PromptColor.setter
    @abstractmethod
    def PromptColor(self, value: Color) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def ErrorColor(self) -> Color:
        """Prompt Color. For OutputType.Error"""
        raise NotImplementedError

    @ErrorColor.setter
    @abstractmethod
    def ErrorColor(self, value: Color) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def OkColor(self) -> Color:
        """Prompt Color. For OutputType.OK"""
        raise NotImplementedError

    @OkColor.setter
    @abstractmethod
    def OkColor(self, value: Color) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def TitleColor(self) -> Color:
        """Prompt Color. For OutputType.Title"""
        raise NotImplementedError

    @TitleColor.setter
    @abstractmethod
    def TitleColor(self, value: Color) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def InformationColor(self) -> Color:
        """Prompt Color. For OutputType.Info"""
        raise NotImplementedError

    @InformationColor.setter
    @abstractmethod
    def InformationColor(self, value: Color) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def SystemColor(self) -> Color:
        """Prompt Color. For OutputType.System"""
        raise NotImplementedError

    @SystemColor.setter
    @abstractmethod
    def SystemColor(self, value: Color) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def WarningColor(self) -> Color:
        """Prompt Color. For OutputType.System"""
        raise NotImplementedError

    @WarningColor.setter
    @abstractmethod
    def WarningColor(self, value: Color) -> None:
        raise NotImplementedError

    @staticmethod
    def DefaultColorSetting():
        """Default color settings for IOServer."""
        return ColorSetting(
            DefaultColor=Color('White'),
            ErrorColor=Color('Red'),
            PromptColor=Color('Magenta'),
            OkColor=Color('Green'),
            TitleColor=Color('YellowGreen'),
            InformationColor=Color('DarkCyan'),
            SystemColor=Color('DarkBlue'),
            WarningColor=Color('Orange'),
            BackgroundColor=Color('Black')
        )

    @abstractmethod
    def __eq__(self, that: object) -> bool:
        """Indicates whether this instance and a specified object are equal.

        :param that: The object to compare with the current instance.
        """
        raise NotImplementedError

    @staticmethod
    def SelectColor(colorSetting, otype: OutputType = OutputType.Default, customColor: Optional[Color] = None) -> Color:
        """select color for the output type from color setting

        :param colorSetting: color setting
        :param otype: output type
        :param customColor: customized color
        """
        if customColor is not None:
            return customColor
        if otype == OutputType.Default:
            return colorSetting.DefaultColor
        elif otype == OutputType.Prompt:
            return colorSetting.PromptColor
        elif otype == OutputType.Error:
            return colorSetting.ErrorColor
        elif otype == OutputType.Ok:
            return colorSetting.OkColor
        elif otype == OutputType.Title:
            return colorSetting.TitleColor
        elif otype == OutputType.Info:
            return colorSetting.InformationColor
        elif otype == OutputType.System:
            return colorSetting.SystemColor
        elif otype == OutputType.Warning:
            return colorSetting.WarningColor
        else:
            return colorSetting.BackgroundColor


class ColorSetting(IColorSetting):
    """Color settings of a Mobile Suit."""

    def __init__(self, BackgroundColor: Color, DefaultColor: Color, PromptColor: Color, ErrorColor: Color,
                 OkColor: Color, TitleColor: Color, InformationColor: Color, SystemColor: Color, WarningColor: Color):
        self._BackgroundColor = BackgroundColor
        self._DefaultColor = DefaultColor
        self._PromptColor = PromptColor
        self._ErrorColor = ErrorColor
        self._OkColor = OkColor
        self._TitleColor = TitleColor
        self._InformationColor = InformationColor
        self._SystemColor = SystemColor
        self._WarningColor = WarningColor

    @property
    def BackgroundColor(self) -> Color:
        """BackgroundColor"""
        return self._BackgroundColor

    @BackgroundColor.setter
    def BackgroundColor(self, value: Color) -> None:
        self._BackgroundColor = value

    @property
    def DefaultColor(self) -> Color:
        """Default color. For OutputType.Default"""
        return self._DefaultColor

    @DefaultColor.setter
    def DefaultColor(self, value: Color) -> None:
        self._DefaultColor = value

    @property
    def PromptColor(self) -> Color:
        """Prompt Color. For OutputType.Prompt"""
        return self._PromptColor

    @PromptColor.setter
    def PromptColor(self, value: Color) -> None:
        self._PromptColor = value

    @property
    def ErrorColor(self) -> Color:
        """Prompt Color. For OutputType.Error"""
        return self._ErrorColor

    @ErrorColor.setter
    def ErrorColor(self, value: Color) -> None:
        self._ErrorColor = value

    @property
    def OkColor(self) -> Color:
        """Prompt Color. For OutputType.AllOK"""
        return self._OkColor

    @OkColor.setter
    def OkColor(self, value: Color) -> None:
        self._OkColor = value

    @property
    def TitleColor(self) -> Color:
        """Prompt Color. For OutputType.ListTitle"""
        return self._TitleColor

    @TitleColor.setter
    def TitleColor(self, value: Color) -> None:
        self._TitleColor = value

    @property
    def InformationColor(self) -> Color:
        """Prompt Color. For OutputType.CustomInformation"""
        return self._InformationColor

    @InformationColor.setter
    def InformationColor(self, value: Color) -> None:
        self._InformationColor = value

    @property
    def SystemColor(self) -> Color:
        """Prompt Color. For OutputType.Information"""
        return self._SystemColor

    @SystemColor.setter
    def SystemColor(self, value: Color) -> None:
        self._SystemColor = value

    @property
    def WarningColor(self) -> Color:
        """Warning color. For OutputType.Warning"""
        return self._WarningColor

    @WarningColor.setter
    def WarningColor(self, value: Color) -> None:
        self._WarningColor = value

    def Equals(self, other: Optional[IColorSetting]) -> bool:
        """Indicates whether this instance and a specified object are equal.
        
        :param other: The object to compare with the current instance.
        """
        return other is not None and \
            self.DefaultColor == other.DefaultColor and \
            self.PromptColor == other.PromptColor and \
            self.ErrorColor == other.ErrorColor and \
            self.OkColor == other.OkColor and \
            self.TitleColor == other.TitleColor and \
            self.InformationColor == other.InformationColor and \
            self.SystemColor == other.SystemColor and \
            self.WarningColor == other.WarningColor and \
            self.BackgroundColor == other.BackgroundColor

    def __eq__(self, that: object) -> bool:
        """Indicates whether this instance and a specified object are equal.
        
        :param that: The object to compare with the current instance.
        """
        return isinstance(that, IColorSetting) and self.Equals(that)

    def __hash__(self) -> int:
        """generate hash code of all colors
        
        :returns: hash code of all colors
        """
        return hash((self.DefaultColor, self.PromptColor, self.ErrorColor, self.OkColor, self.TitleColor,
                     self.InformationColor, self.SystemColor, self.WarningColor, self.BackgroundColor))

    def __ne__(self, that: object) -> bool:
        """Indicates whether two instances are not-equal.
        
        :param that: The object to compare with the current instance.
        """
        return not (self == that)
