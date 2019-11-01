#!/usr/bin/env python
import os
import random
from pathlib import Path

lines = open(f'{Path.home()}/scripts/lock/lines')
line = random.choice(lines.read().splitlines())
lines.close()

os.system(f'betterlockscreen -l dimblur -t \"{line}\"')
