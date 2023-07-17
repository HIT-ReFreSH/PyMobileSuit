from enum import Enum

class OutputType(Enum):
    """Type of content that writes to the output stream."""
    Default = 0
    """Normal content."""
    Prompt = 1
    """Prompt content."""
    Error = 2
    """Error content."""
    Ok = 3
    """All-Ok content."""
    Title = 4
    """Title of a list."""
    Info = 5
    """Normal information."""
    System = 6
    """Information provided by MobileSuit."""
    Warning = 7
    """Warning content."""
