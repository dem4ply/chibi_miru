#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'chibi>=0.12.1', 'opencv-python>=4.5.5', 'pyzbar>=0.1.8',
    'pillow>=11.0.0', 'pytesseract>=0.3.13' ]

setup(
    author="dem4ply",
    author_email='dem4ply@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="poder usar la camara y leerla como si fuera un objeto usando opencv",
    entry_points={
        'console_scripts': [
            'chibi_miru=chibi_miru.cli:main',
        ],
    },
    install_requires=requirements,
    license="WTFPL",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='chibi_miru',
    name='chibi_miru',
    packages=find_packages(include=['chibi_miru', 'chibi_miru.*']),
    url='https://github.com/dem4ply/chibi_miru',
    version='0.0.1',
    zip_safe=False,
)
