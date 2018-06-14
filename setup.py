#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='app',
    version='0.9',
    description="",
    author="Anton",
    author_email='anton@vidispine.com',
    url='',
    packages=find_packages(),
    package_data={'app': ['static/*.*', 'templates/*.*']},
    scripts=['manage.py'], install_requires=['requests', 'django', 'lxml']
)
