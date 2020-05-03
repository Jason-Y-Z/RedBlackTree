#!/usr/bin/env python

from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='red_black_tree',
    version='0.0.1',
    description='Python Red Black Tree',
    author='Jason Zhang',
    author_email='jasonzhang2013@outlook.com',
    url='https://github.com/LowkeyDefun/RedBlackTree',
    packages=['red_black_tree'],
    license='MIT license',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
