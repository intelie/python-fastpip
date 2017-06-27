#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


class Tox(TestCommand):
    user_options = TestCommand.user_options + [
        ('environment=', 'e', "Run 'test_suite' in specified environment")
    ]
    environment = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        if self.environment:
            self.test_args.append('-e{0}'.format(self.environment))
        errno = tox.cmdline(self.test_args)
        sys.exit(errno)


def read_file(filename):
    """Read a file into a string"""
    open_kwargs = {}
    if sys.version_info.major == 3:
        open_kwargs = {'encoding': 'utf-8'}

    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    with open(filepath, **open_kwargs) as filecontents:
        return filecontents.read()


def get_readme():
    """Return the README file contents. Supports text,rst, and markdown"""
    for name in ('README', 'README.rst', 'README.md'):
        if os.path.exists(name):
            return read_file(name)
    return ''


setup(
    name="python-fastpip",
    version="1.2",
    url='https://github.com/intelie/python-fastpip',
    author='Vitor M. A. da Cruz',
    author_email='vitor.mazzi@intelie.com.br',
    description='Segmentation Based On Turning Points',
    long_description=get_readme(),
    packages=find_packages(exclude=["example", "*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires='',
    tests_require=['virtualenv>=1.11.2', 'tox>=1.6.1', ],
    cmdclass={'test': Tox},
    test_suite='fastpip.tests',
    classifiers=[
        'Topic :: Scientific/Engineering :: Visualization',
        'License :: OSI Approved :: Apache Software License',
    ],
    license="Apache 2",
)
