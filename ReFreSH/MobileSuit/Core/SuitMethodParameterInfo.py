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


class SuitMethodParameterInfo(object):
    """
    Parameter information of a method in MobileSuit
    """

    def __init__(self):
        self.TailParameterType: TailParameterType = TailParameterType.NoParameter
        """
        Type of the last parameter
        """

        self.MinParameterCount: int = 0
        """
        Number of the parameters which can be passed at most.
        """

        self.NonArrayParameterCount: int = 0
        """
        Number of the parameters which are neither array nor DynamicParameter
        """

        self.MaxParameterCount: int = 0
        """
        Number of the parameters which can be passed at least.
        """
