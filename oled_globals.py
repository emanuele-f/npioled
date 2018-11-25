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

SCREEN_SIZE = (128, 64)

INPUT_TYPE = {
  "NONE": 0,
  "BTN_LEFT": 1,
  "BTN_CENTER": 2,
  "BTN_RIGHT": 3,
}

SLEEP_MS = 250

# Note: update time ~= SLEEP_MS * TICKS_BEFORE_UPDATE
TICKS_BEFORE_UPDATE = 8

# TODO add more strict check
try:
  import smbus
except ImportError:
  DISPLAY_BACKEND = "wx_backend"
  DISPLAY_DPI = 96
else:
  DISPLAY_BACKEND = "oled_backend"
  DISPLAY_DPI = 80
