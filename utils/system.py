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

import subprocess
import struct
import socket
import fcntl

def getPid(name):
  try:
    return int(subprocess.check_output(["pidof", "-s", name]))
  except subprocess.CalledProcessError:
    return None

def getIpAddress(ifname):
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  return socket.inet_ntoa(fcntl.ioctl(
      s.fileno(),
      0x8915,  # SIOCGIFADDR
      struct.pack('256s', ifname[:15]))[20:24])

def getCpuTemp():
  return int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1000

def getCpuFreq():
  with open("/sys/devices/system/cpu/cpu0/cpufreq/cpuinfo_cur_freq") as f:
    freq = int(f.readlines()[0])/1000
    freqStr = "%d MHz" % freq
    if freq > 1000:
      freqStr = "%.1f GHz" % (float(freq)/1000.0)
    return freqStr
