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

import signal

from oled_globals import *
import third_party.bakebit_128_64_oled as oled
import RPi.GPIO as GPIO

LEFT_BTN_PIN = 11
CENTER_BTN_PIN = 13
RIGHT_BTN_PIN = 15

_key_pressed = {}

# NOT_USED
def _handle_signal(signum, stack):
  key = None

  if signum == signal.SIGUSR1:
    key = INPUT_TYPE["BTN_LEFT"]
  elif signum == signal.SIGHUP:
    key = INPUT_TYPE["BTN_CENTER"]
  elif signum == signal.SIGUSR2:
    key = INPUT_TYPE["BTN_RIGHT"]

  if key:
    _key_pressed[key] = True

# NOT_USED
def getInput():
  for key in _key_pressed:
    del _key_pressed[key]
    return key
  return INPUT_TYPE["NONE"]

def getInput():
 if GPIO.input(LEFT_BTN_PIN): return INPUT_TYPE["BTN_LEFT"]
 elif GPIO.input(RIGHT_BTN_PIN): return INPUT_TYPE["BTN_RIGHT"]
 elif GPIO.input(CENTER_BTN_PIN): return INPUT_TYPE["BTN_CENTER"]
 else: return INPUT_TYPE["NONE"]

def clearInputs():
  # TODO
  pass

def drawImage(pil_image):
  oled.drawImage(pil_image)

def tick():
  pass

def init():
  oled.init()                  #initialze SEEED OLED display
  oled.setNormalDisplay()      #Set display to normal mode (i.e non-inverse mode)
  oled.setHorizontalMode()
  # oled.setPageMode() # This allows to reason on a line mode rather than graphical mode
  oled.clearDisplay()          #clear the screen and set start position to top left corner

  # Note the async mode of reading the buttons is buggy, so we will read them manually
  #signal.signal(signal.SIGUSR1, _handle_signal)
  #signal.signal(signal.SIGUSR2, _handle_signal)
  #signal.signal(signal.SIGHUP, _handle_signal)

  GPIO.setmode(GPIO.BOARD)
  GPIO.setup(LEFT_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(RIGHT_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
  GPIO.setup(CENTER_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
