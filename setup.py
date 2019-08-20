'''
Auto-generated setup.py for python_morph package.

'''

import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    '''helper to read long description out of README.md'''
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as infile:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), infile.read())


setup(
    name="python_morph",
    version="0.1.0",
    url="https://github.com/netserf/python-morph",
    license='MIT',

    author="Greg Horie",
    author_email="networkserf@gmail.com",

    description="For those that don't like the one-liner awk or perl options, " \
        "this is a command line tool that helps you manage your string" \
        "transformations through a yaml config file.",
    long_description=read("README.md"),

    packages=find_packages(exclude=('tests',)),

    install_requires=[],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
