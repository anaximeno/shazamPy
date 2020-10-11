#!/usr/bin/env python3


from setuptools import setup


setup(
    name='checksum',
    version='0.1.9',
    author='Anaxímeno Brito',
    author_email='anaximenobrito@gmail.com',
    url='https://github.com/anaximeno/checksum',
    packages=['checksum'],
    install_requires=[
        'hashlib',
        'alive_progress',
        'termcolor',
        'os',
        'time'
        ],
)
