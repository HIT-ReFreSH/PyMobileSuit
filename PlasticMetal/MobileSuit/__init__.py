from . import Suit
from .Decorators import *
from .IIOHub import IIOHub
from ..CSharp import nameof

__all__ = [nameof(x) for x in [Suit, SuitInfo, SuitIgnore, SuitAlias, SuitArgInjected, SuitArgParser, IIOHub]]
__version__ = '0.1'
__author__ = 'Ferdinand Sukhoi'
