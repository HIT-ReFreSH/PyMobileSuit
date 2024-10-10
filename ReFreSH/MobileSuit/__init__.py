from . import Suit, SuitConfig
from .Decorators import SuitInfo, SuitIgnore, SuitAlias, SuitArgInjected, SuitArgParser
from .IIOHub import IIOHub
from ..CSharp import nameof

__all__ = [nameof(x) for x in [Suit, SuitInfo, SuitIgnore, SuitAlias, SuitArgInjected, SuitArgParser, IIOHub, SuitConfig]]
__version__ = '0.1'
__author__ = 'Ferdinand Sukhoi'
