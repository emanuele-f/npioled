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

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from time import sleep

import backend as backend
from oled_globals import *
import utils
import psutil
import platform
import multiprocessing
import numpy as np

backend = backend.getBackend()

sleep_sec = SLEEP_MS / 1000.
update_ticks = 0

ACTIVE_STAGE = None
INPUT_DISABLED = False

small_font_size = 10
small_font = ImageFont.truetype('DejaVuSansMono-Bold.ttf', small_font_size)

def switch_stage(stage_cls):
  global ACTIVE_STAGE
  global update_ticks

  if ACTIVE_STAGE: ACTIVE_STAGE.leave()
  ACTIVE_STAGE = stage_cls()
  ACTIVE_STAGE.enter()
  ACTIVE_STAGE.update()
  update_ticks = 0

def set_input_enabled(enabled):
  global INPUT_DISABLED
  INPUT_DISABLED = not enabled

# -----------------------------------------------------------------------------

class Stage():
  def tick(self): pass
  def update(self): pass
  def enter(self): pass
  def leave(self): pass

  # TODO
  def leftButton(self): switch_stage(SysInfoStage)
  def centerButton(self): switch_stage(TrafficChartStage)
  def rightButton(self): switch_stage(TrafficBarChart)

class SysInfoStage(Stage):
  def update(self):
    ip_address = utils.system.getIpAddress("eth0")
    cpu_freq = utils.system.getCpuFreq()
    memUsage = psutil.virtual_memory()
    diskUsage = psutil.disk_usage('/')
    temperature = utils.system.getCpuTemp()

    image = utils.draw.newImage()
    context = ImageDraw.Draw(image)

    utils.draw.drawText(context, [
      "IP: %s" % ip_address,
      "Mem Tot: %s" % utils.draw.bytesToSize(memUsage.total),
      "Mem Free: %s" % utils.draw.bytesToSize(memUsage.free),
      "Temp: %d *C" % temperature,
      "CPU: %s%%" % psutil.cpu_percent(),
      "Freq: %s" % cpu_freq,
    ], small_font, small_font_size)

    backend.drawImage(image)

class TrafficBarChart(Stage):
  def update(self):
    traffic_chart = utils.draw.stackedBarChart([
      np.random.randint(0, 100, 10), # up bytes
      np.random.randint(0, 100, 10), # down bytes
    ])

    backend.drawImage(traffic_chart)

class TrafficChartStage(Stage):
  def update(self):
    y_offset = 25

    traffic_chart = utils.draw.stackedLineChart([
      np.random.randint(0, 100, 10), # up bytes
      np.random.randint(0, 100, 10), # down bytes
    ], size=(SCREEN_SIZE[0], SCREEN_SIZE[1] - y_offset))

    image = utils.draw.newImage()
    image.paste(traffic_chart, (0, y_offset))
    context = ImageDraw.Draw(image)

    utils.draw.drawText(context, [
      "Up: %s" % "111.2 Mbit/s",
      "Down: %s" % "151.1 Mbit/s"],
      small_font, small_font_size, x=2, y=1)
    backend.drawImage(image)

class SplashScreen(Stage):
  def enter(self):
    set_input_enabled(False)

  def update(self):
    image = Image.open('assets/logo.png').convert('1')
    backend.drawImage(image)

  def leave(self):
    sleep(3)
    set_input_enabled(True)

  def tick(self):
    switch_stage(TrafficChartStage)

# -----------------------------------------------------------------------------

switch_stage(SplashScreen)

while True:
  backend.tick()

  if not INPUT_DISABLED:
    button = backend.getInput()

    if button != INPUT_TYPE["NONE"]:
      if button == INPUT_TYPE["BTN_LEFT"]:
        ACTIVE_STAGE.leftButton()
      elif button == INPUT_TYPE["BTN_RIGHT"]:
        ACTIVE_STAGE.rightButton()
      elif button == INPUT_TYPE["BTN_CENTER"]:
        ACTIVE_STAGE.centerButton()
      else:
        print("WARNING: unknown button " + button)
  else:
    backend.clearInputs()

  update_ticks += 1

  ACTIVE_STAGE.tick()
  if update_ticks >= TICKS_BEFORE_UPDATE:
    ACTIVE_STAGE.update()
    update_ticks = 0

  sleep(sleep_sec)
