#!/usr/bin/env python

from subprocess import Popen

event_handler_process = Popen(["./event_handler.py"])
broadcaster_process = Popen(["./broadcaster.py"])

input()

event_handler_process.kill()
broadcaster_process.kill()
