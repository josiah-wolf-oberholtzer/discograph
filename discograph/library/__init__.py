# -*- encoding: utf-8 -*-
from abjad.tools import systemtools

from discograph.library.postgres import *

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )