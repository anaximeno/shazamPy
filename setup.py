#!/usr/bin/python2

__version__ = "0.2.0"

from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="checksum",
    version=__version__,
    author="Anaximeno Brito",
    author_email="anaximenobrito@gmail.com",
    url="https://github.com/anaximeno/checksum",
    packages=["checksum"],
    install_requires=[
        "alive_progress>=1.6.1",
        "termcolor>=1.1.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
        },
)
