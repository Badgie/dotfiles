#!/usr/bin/env python
import os
import random

lines = open('/home/badgy/scripts/lock/lines')
line = random.choice(lines.read().splitlines())
lines.close()

os.system('betterlockscreen -l dimblur -t \"' + line + '\"')
