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

from oled_globals import *

wx = None

_bitmapWidget = None
_wximage = None
_app = None
_loop = None
_key_pressed = {}

def _keydown_handler(event):
  #keycode = event.GetKeyCode()
  try:
    key = chr(event.GetKeyCode())
  except ValueError:
    key = None

  if key == "Q":
    button = INPUT_TYPE["BTN_LEFT"]
  elif key == "W":
    button = INPUT_TYPE["BTN_CENTER"]
  elif key == "E":
    button = INPUT_TYPE["BTN_RIGHT"]
  else:
    button = None

  if button:
    _key_pressed[button] = True

def _close_handler(event):
  exit(0)

# ------------------------------------------------------------------------------

def getInput():
  for key in _key_pressed:
    del _key_pressed[key]
    return key
  return INPUT_TYPE["NONE"]

def clearInputs():
  _key_pressed = {}

def drawImage(pil_image):
  #_wximage.SetData(pil_image.convert('1', dither=Image.NONE).convert('RGB').tobytes())
  _wximage.SetData(pil_image.convert('RGB').tobytes())
  _bitmapWidget.SetBitmap(_wximage.ConvertToBitmap())
  _bitmapWidget.Parent.Update()

def tick():
  # Displatch all the events
  while _loop.Pending():
    _loop.Dispatch()
  _loop.ProcessIdle()

def init():
  global wx
  global _bitmapWidget
  global _wximage
  global _loop
  global _app

  import wxversion
  wxversion.select("3.0")
  import wx

  _app = wx.App(False)
  frame = wx.Frame(None, wx.ID_ANY)
  panel = wx.Panel(frame, wx.ID_ANY)
  _wximage = wx.EmptyImage(SCREEN_SIZE[0], SCREEN_SIZE[1])
  _bitmapWidget = wx.StaticBitmap(panel, bitmap=_wximage.ConvertToBitmap())
  box = wx.BoxSizer(wx.VERTICAL)
  box.Add(panel)
  frame.SetSizerAndFit(box)

  panel.Bind(wx.EVT_KEY_DOWN, _keydown_handler)
  frame.Bind(wx.EVT_CLOSE, _close_handler)
  frame.Show(True)

  _loop = wx.GUIEventLoop()
  wx.EventLoop.SetActive(_loop)
