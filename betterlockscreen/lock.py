#!/usr/bin/env python
import os
import random
from pathlib import Path

with open(f'{Path.home()}/scripts/lock/lines') as file:
    os.system(f'betterlockscreen -l dimblur -t \"{random.choice(file.read().splitlines())}\"')
