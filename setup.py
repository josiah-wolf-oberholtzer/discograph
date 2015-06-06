#! /usr/bin/env python

from distutils.core import setup


if __name__ == '__main__':
    setup(
        author='Josiah Wolf Oberholtzer',
        author_email='josiah.oberholtzer@gmail.com',
        install_requires=[
            'discogs-client',
            'pytest',
            ],
        license='MIT',
        name='discgraph',
        packages=[
            'discgraph',
            ],
        )