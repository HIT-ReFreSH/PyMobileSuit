from typing import List

from .SuitHostBuilder import SuitHostBuilder


def QuickStart4BitPowerLine(T, args: List[str] = []):
    """Quick start a mobilesuit on specific client class with 4bit IO and PowerLine"""
    CreateBuilder(args).HasName("demo").UsePowerLine().Use4BitColorIO().MapClass(T).Build().Run()


def QuickStart(T, args: List[str] = []):
    """Quick start a mobilesuit on specific client class with default settings."""
    CreateBuilder(args).HasName("demo").UsePowerLine().Use4BitColorIO().MapClass(T).Build().Run()


def QuickStartPowerLine(T, args: List[str] = []):
    """Quick start a mobilesuit on specific client class with PowerLine"""
    CreateBuilder(args).HasName("demo").UsePowerLine().MapClass(T).Build().Run()


def CreateBuilder(args: List[str] = None) -> SuitHostBuilder:
    """Get a builder to create host"""
    return SuitHostBuilder(args)
