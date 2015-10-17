# -*- encoding: utf-8 -*-
import os


class Configuration(object):
    DEBUG = False
    TESTING = False
    APPLICATION_ROOT = 'http://discograph.mbrsi.org'
    FILE_CACHE_PATH = os.path.join(os.path.dirname(__file__), '..', 'tmp')
    FILE_CACHE_THRESHOLD = 1024 * 128
    FILE_CACHE_TIMEOUT = 60 * 60 * 48


class DevelopmentConfiguration(Configuration):
    DEBUG = True
    TESTING = True


__all__ = [
    'Configuration',
    'DevelopmentConfiguration',
    ]