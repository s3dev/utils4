# -*- coding: utf-8 -*-

import sys
from utils4._version import __version__

# Initialise colorama for Windows only.
if sys.platform == 'win32':  # pragma: nocover
    import colorama
    colorama.init()
