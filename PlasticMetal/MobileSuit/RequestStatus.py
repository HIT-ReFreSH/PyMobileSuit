from enum import IntEnum


class RequestStatus(IntEnum):
    NoRequest = 1
    """
    No Request is input by the user.
    """

    OnExit = -1
    """
    The Progress is Exiting
    """

    Ok = 0
    """
    Everything is OK
    """

    NotHandled = 2
    """
    No Request is input by the user.
    """

    Running = 3
    """
    Command is Running. Set by the FinalMiddleware.
    """

    Handled = 4
    """
    Command is Running. Set by the FinalMiddleware.
    """

    Interrupt = -2
    """
    Cannot find the object referring to.
    """

    CommandNotFound = -3
    """
    Cannot find the member in the object referring to.
    """

    Faulted = -4
    """
    Error in the application
    """

    CommandParsingFailure = -5
    """
    Failed to parse an argument of a command.
    """
