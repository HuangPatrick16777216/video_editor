#
#  Pymixer
#  Video editor with a Python API.
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import sys
import os
import importlib


def register(dirs):
    for d in dirs:
        if os.path.isdir(d):
            sys.path.append(d)
            for f in os.listdir(d):
                register_module(f)
            sys.path.pop()


def register_module(file):
    try:
        mod = importlib.import_module(os.path.splitext(file)[0])
        mod.register()
    except AttributeError:   # Tried to import __pycache__
        pass
