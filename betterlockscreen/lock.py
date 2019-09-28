#!/usr/bin/env python
import os
import random

lines = open('/home/badgy/scripts/lock/lines').read().splitlines()
line = random.choice(lines)

os.system('betterlockscreen -l dimblur -t \"' + line + '\"')
