#!/usr/bin/env python2
#
# ----------------------------------------------------------------------------
# npioled - A library to interact with the Nano PI OLED hat
# ----------------------------------------------------------------------------
#
# Copyright (C) 2018 - Emanuele Faranda
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.
#

_backends_api = {
  "init": """Initializes the backend.""",
  "drawImage": """Draws a PIL image on the screen. The image must be SCREEN_SIZE wide.""",
  "tick": """One tick of the app loop.""",
  "getInput": """Returns one of the INPUT_TYPE result.""",
  "clearInputs": """Clear any pending inputs.""",
}

from oled_globals import DISPLAY_BACKEND

import sys
sys.path.insert(1, "backend")

import importlib
_backend = importlib.import_module(DISPLAY_BACKEND)

def getBackend():
  return _backend

# Verify API
for api in _backends_api:
  try:
    getattr(_backend, api)
  except AttributeError:
    print("ERROR: Missing API '" + api + "' in backend '" + DISPLAY_BACKEND + "'")
    exit(1)

_backend.init()
