#!/usr/bin/env python
"""
 *  NOTE      - save_randr.py
 *  Author    - Aru
 *
 *  Created   - 2023.04.04
 *  Github    - https://github.com/aruyu
 *  Contact   - vine9151@gmail.com
"""

import os
import subprocess


def save_screenrc():
  """ Function to Save Screen RC """

  xrandr_current = subprocess.run(["xrandr", "--current"], shell=True, text=True, stdout=subprocess.PIPE).stdout
  xrandr_current_list = xrandr_current.split('\n')
  xrandr_connected_index = []
  command = "xrandr"
  retval = ""

  for key, value in enumerate(xrandr_current_list):
    if "connected" in value.split(' '):
      xrandr_connected_index.append(key)

  for i in xrandr_connected_index:
    base_value = xrandr_current_list[i].split(' ')
    output_value = base_value[0]

    if base_value[2] == "primary":
      mode_pos_list = base_value[3]
      rotate_list = base_value[4]
    else:
      mode_pos_list = base_value[2]
      rotate_list = base_value[3]

    if not mode_pos_list.startswith('('):
      mode_pos_list = mode_pos_list.split('+')

      mode_list = mode_pos_list[0]
      mode_list = mode_list.split('x')
      mode_x_value = mode_list[0]
      mode_y_value = mode_list[1]

      if int(mode_x_value) < int(mode_y_value):
        mode_x_value, mode_y_value = mode_y_value, mode_x_value
      mode_value = mode_x_value + 'x' + mode_y_value

      pos_x_value = mode_pos_list[1]
      pos_y_value = mode_pos_list[2]

      if not rotate_list.startswith('('):
        rotate_value = rotate_list
      else:
        rotate_value = "normal"

      command += " --output {0} --mode {1} --pos {2}x{3} --rotate {4}".format(output_value, mode_value, pos_x_value, pos_y_value, rotate_value)
      retval += "{0}: {1} ({2})".format(output_value, mode_value, rotate_value)
    else:
      command += " --output {0} --off".format(output_value)
      retval += "{0}: Off".format(output_value)
    retval += '\n'

  home_directory = os.path.expanduser('~')
  script_file = open(home_directory+"/.screenlayout/rcscript", 'w')
  script_file.writelines('\n'.join(["#!/bin/bash", "", command]))
  script_file.close()

  return retval

if __name__ == '__main__':
  try:
    command = save_screenrc()
  except:
    try:
      os.system('mkdir ~/.screenlayout')
      command = save_screenrc()
    except:
      os.system('notify-send --urgency critical "Save Display" "Failed to save display settings." --icon="tint2"')
      raise
  finally:
    os.system('notify-send "Save Display" "Current display successfully saved to ~/.screenlayout/rcscript.\n\n' + \
              '[Current]\n' + command + '" --icon="tint2"')
