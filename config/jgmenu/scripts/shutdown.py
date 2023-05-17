#!/usr/bin/env python
"""
 *  NOTE      - shutdown.py
 *  Author    - Aru
 *
 *  Created   - 2023.04.04
 *  Github    - https://github.com/aruyu
 *  Contact   - vine9151@gmail.com
"""

import time
import threading
import os
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk,GLib


class ShutdownDialog(Gtk.Dialog):
  def __init__(self, parent):
    super().__init__(title="Shut Down", transient_for=parent, flags=0)
    self.add_button("Cancel", Gtk.ResponseType.CANCEL)
    self.add_button("Reboot", Gtk.ResponseType.YES)
    self.add_button("Shutdown", Gtk.ResponseType.OK)

    self.set_default_size(350, 100)

    self.shutdown_countdown = CountdownThread()
    self.shutdown_countdown.daemon = True
    self.shutdown_countdown.start()

    label = self.shutdown_countdown.label

    box = self.get_content_area()
    box.add(label)
    self.show_all()


class DialogWindow(Gtk.Window):
  def __init__(self):
    Gtk.Window.__init__(self, title="")
    self.on_button_clicked()

  def on_button_clicked(self):
    dialog = ShutdownDialog(self)
    response = dialog.run()

    if response == Gtk.ResponseType.OK:
      os.system("sync ; sync ; sync ; sync ; halt --poweroff")
    elif response == Gtk.ResponseType.YES:
      os.system("sync ; sync ; sync ; sync ; halt --reboot")

    dialog.destroy()


def quit_time_out():
  Gtk.main_quit()
  return False


class CountdownThread(threading.Thread):
  """ Class of Countdown Thread. """

  def __init__(self, name=0, time_out=61):
    super().__init__()
    self.name = name
    self.time_out = time_out
    self.label = Gtk.Label()

  def run(self):
    """ Function to Run """

    while self.time_out:
      self.time_out -= 1
      self.label.set_text("The system will be shut down in {0} seconds.".format(self.time_out))
      time.sleep(1)

    os.system("sync ; sync ; sync ; sync ; halt --poweroff")


if __name__ == '__main__':
  win = DialogWindow()
  GLib.timeout_add(10, quit_time_out)
  Gtk.main()
