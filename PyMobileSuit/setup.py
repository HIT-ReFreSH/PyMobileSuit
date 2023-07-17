#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   setup.py
@Contact :   ferdinandsukhoi@outlook.com
@License :   (C)Copyright 2020 Plastic-Metal

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-5-15   Ferdinand Sukhoi      0.1.4   Light-weight tool to generate markdown-formatted lab reports.
"""

from setuptools import setup, find_packages

setup(
    name = "pylabon",
    version = "0.1.4.3",
    keywords = ["markdown", "Plastic-Metal"],
    description = "To generate markdown-formatted lab reports.",
    long_description = "Light-weight tool to generate markdown-formatted lab reports. For python.",
    license = "MIT",

    url = "https://github.com/Plastic-Metal/pyLabOn",
    author = "Ferdinand Sukhoi",
    author_email = "ferdinandsukhoi@outlook.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["colour"]
)
