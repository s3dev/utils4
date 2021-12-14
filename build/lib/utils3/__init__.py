# -*- coding: utf-8 -*-

import sys
from utils3._version import __version__

# Initialise colorama for Windows only.
if sys.platform == 'win32':
    import colorama
    colorama.init()
