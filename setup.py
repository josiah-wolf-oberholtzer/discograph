#! /usr/bin/env python

import setuptools


if __name__ == '__main__':
    setuptools.setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        include_package_data=True,
        install_requires=[
            'PyMySQL',
            'abjad',
            'flask',
            'mongoengine',
            'peewee',
            'pytest',
            'python-levenshtein',
            'python-memcached',
            'six',
            ],
        license='MIT',
        name='discograph',
        packages=[
            'discograph',
            ],
        )