#! /usr/bin/env python

from distutils.core import setup


if __name__ == '__main__':
    setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        install_requires=[
            'abjad',
            'flask',
            'mongoengine',
            'pytest',
            'six',
            ],
        license='MIT',
        name='discograph',
        packages=[
            'discograph',
            ],
        )