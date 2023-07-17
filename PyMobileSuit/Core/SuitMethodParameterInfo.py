from enum import IntEnum

class TailParameterType(IntEnum):
    """
    Represents type of the last parameter of a method
    """

    Normal = 0
    """
    Last parameter exists, and is quite normal.
    """

    Array = 1
    """
    Last parameter is an array.
    """
    # TODO: DynamicParameter support
    # DynamicParameter = 2
    # """
    # Last parameter implements IDynamicParameter.
    # """

    NoParameter = -1
    """
    Last parameter does not exist.
    """

from typing import NamedTuple

class SuitMethodParameterInfo(NamedTuple):
    """
    Parameter information of a method in MobileSuit
    """
    TailParameterType: TailParameterType
    """
    Type of the last parameter
    """

    MinParameterCount: int
    """
    Number of the parameters which can be passed at most.
    """

    NonArrayParameterCount: int
    """
    Number of the parameters which are neither array nor DynamicParameter
    """

    MaxParameterCount: int
    """
    Number of the parameters which can be passed at least.
    """
