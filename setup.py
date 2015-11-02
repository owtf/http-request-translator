#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='http_request_translator',
    version='0.1',
    description='Translates raw HTTP requests to Python,Ruby,Php and Bash scripts',
    url='https://github.com/owtf/http-request-translator/',
    author='Ramana Subramanyam, Arun Sori, cjdupreez',
    author_email='owasp_owtf_developers@lists.owasp.org',
    license='3-clause BSD',
    install_requires=[],
    packages=['http_request_translator', 'http_request_translator.templates'],
    scripts=['bin/http_request_translator'])
