#!/usr/bin/env python
# coding: utf-8

import os
from setuptools import setup, find_packages

def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

PACKAGE = "vanellope"
NAME = "vanellope"
DESCRIPTION = "Personal publishing system"
AUTHOR = "Qiao Anran"
AUTHOR_EMAIL = "qiaoanran@gmail.com"
URL = "https://github.com/qar/vanellope"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests", "test.*", "test"]),

    include_package_data=True,

    install_requires=[
      'tornado',
      'pytz',
      'user_agents',
      'python-dateutil',
    ],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
    ],
    entry_points={
        'console_scripts': [
            'vanellope = vanellope.app:main'
        ]
    },
    zip_safe=True,
)
