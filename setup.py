#!/usr/bin/env python3

from setuptools import setup

setup(
    name='seq-id',
    version='1.0',
    description='Species identification engine',
    classifiers=[
        'Programming Language :: Python :: 3.7',
    ],
    url='https://gitlab.mff.cuni.cz/dorcakot/seq-id',
    install_requires=[
        'biopython',
        'requests'
    ],
    include_package_data=True,
    zip_safe=False,
    packages=[
        'seq-id',
    ],
    entry_points={
        'console_scripts': [
            'seq-id=seq-id.main:main',
        ],
    },
)

