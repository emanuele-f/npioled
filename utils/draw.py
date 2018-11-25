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

import numpy as np
import matplotlib
matplotlib.use('Agg') # no window
import matplotlib.pyplot as plt

# Init
# matplotlib.rcParams['hatch.linewidth'] = 1 # hatching size

from math import log
from PIL import Image
from oled_globals import *

# These are the patterns used to fill chart series
# See http://kitchingroup.cheme.cmu.edu/blog/2013/10/26/Hatched-symbols-in-matplotlib/
# NOTE: repeat the symbol as 5 times to show it properly
HATCHES = ["", "+++++"]

def _dpi_to_pixels(size):
  return (size[0] * 1. / DISPLAY_DPI, size[1] * 1. / DISPLAY_DPI)

def _canvasToImage():
  canvas = plt.get_current_fig_manager().canvas
  canvas.draw()
  pil_image = Image.frombytes('RGB', canvas.get_width_height(), canvas.tostring_rgb()).convert('1')
  plt.close("all") # frees plot windows memory, avoiding leaks
  return pil_image.crop((0, 0, SCREEN_SIZE[0], SCREEN_SIZE[1]))

def _newPlot(size):
  fig = plt.figure(figsize=_dpi_to_pixels(size))
  ax = plt.subplot(111)
  fig.set_facecolor('black')
  plt.axis('off')

  # try to remove the margins
  plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
  return fig, ax

def _countPoints(series):
  for serie in series:
    return len(serie)
  return 0

"""Creates a stackedBarChart."""
def stackedBarChart(series, size=SCREEN_SIZE):
  n_points = _countPoints(series)
  x = np.arange(n_points)
  y = np.zeros(n_points)
  i = 0

  fig, ax = _newPlot(size)

  for serie in series:
    old_y = y
    y = y + serie
    plt.bar(x, serie, color='w', bottom = old_y, hatch=HATCHES[i])
    i = i + 1

  return _canvasToImage()

"""Creates a stackedLineChart Image."""
def stackedLineChart(series, size=SCREEN_SIZE):
  n_points = _countPoints(series)
  y = np.row_stack(series)
  x = np.arange(n_points)

  fig, ax = _newPlot(size)
  stack_plot = ax.stackplot(x, y, colors=('white', ))

  for stack, hatch in zip(stack_plot, HATCHES):
    stack.set_hatch(hatch)

  return _canvasToImage()

def newImage():
  return Image.new('1', SCREEN_SIZE)

def drawText(context, lines, font, font_size, x=0, y=0, y_gap=0):
  if isinstance(lines, str):
    lines = (lines, )

  for line in lines:
    context.text((x, y), line, font=font, fill=255)
    y = y + font_size + y_gap

def bytesToSize(value):
  byteunits = ('B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
  exponent = int(log(value, 1024))
  return "%.1f %s" % (float(value) / pow(1024, exponent), byteunits[exponent])
