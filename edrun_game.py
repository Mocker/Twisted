#! /usr/bin/env python

import sys
import os

#run the map editor

try:
    __file__
except NameError:
    pass
else:
    libdir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'lib'))
    sys.path.insert(0, libdir)
    sys.path.append("lib")

import edmain
reload(edmain)
edmain.main()
