#!/usr/bin/env python
# coding: utf-8

import os
import os.path
from setuptools import setup, find_packages


def read(*paths):
    """Build a file path from *paths* and return the contents."""
    with open(os.path.join(*paths), "r") as f:
        return f.read()


def read_data_files(datadir):
    maps = []
    for dirpath, dirnames, filenames in os.walk(datadir):
        target_path = os.path.join(WWW_PATH, dirpath)
        origin_paths = [os.path.join(dirpath, f) for f in filenames]
        maps.append((target_path, origin_paths))
    return maps


WWW_PATH = "/var/www"
UI_FILES = "./vanellope/themes"
ADMIN_UI_FILES = "./vanellope/admin"
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
    long_description=read("README.rst"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests", "test.*", "test"]),
    data_files=read_data_files(UI_FILES) + read_data_files(ADMIN_UI_FILES),

    include_package_data=True,

    setup_requires=[
        "flake8"
    ],
    install_requires=[
        "tornado==4.3",
        "pytz==2016.4",
        "user_agents==1.0.1",
        "python-dateutil==2.4.2",
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
        "console_scripts": [
            "vanellope = vanellope.app:main"
        ]
    },
    zip_safe=True,
)
