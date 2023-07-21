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
    name="PyMobileSuit",
    version="0.1",
    keywords=["commandline", "cli", "framework", "Plastic-Metal"],
    description="To generate markdown-formatted lab reports.",
    long_description="MobileSuit provides an easy way to build Console App quickly. For python.",
    license="MIT",

    url="https://github.com/Plastic-Metal/PyMobileSuit",
    author="Ferdinand Sukhoi",
    author_email="ferdinandsukhoi@outlook.com",

    packages=find_packages(),
    package_data={
        '':[
            "*Resources/*.yaml",
        ]
    },
    include_package_data=True,
    platforms="any",
    python_requires='>=3.9',
    install_requires=["colour"]
)
