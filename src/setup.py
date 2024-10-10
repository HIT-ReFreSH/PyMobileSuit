#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File    :   setup.py
@Contact :   ferdinandsukhoi@outlook.com
@License :   (C)Copyright 2020 HIT-ReFreSH

@Modify Time      @Author    @Version    @Description
------------      -------    --------    -----------
2020-5-15   Ferdinand Sukhoi      0.1.1   Light-weight tool to generate markdown-formatted lab reports.
"""

from setuptools import setup, find_packages

setup(
    name="PyMobileSuit",
    version="0.1.1",
    keywords=["commandline", "cli", "framework", "HIT-ReFreSH"],
    description="An easy way to build python-CLI App quickly.",
    long_description="MobileSuit provides an easy way to build Console App quickly. For python.",
    license="MIT",

    url="https://github.com/HIT-ReFreSH/PyMobileSuit",
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
