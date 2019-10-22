#!/usr/bin/env python

import subprocess
import re


def get_cpu_status() -> list:
    ps = subprocess.Popen(['sensors'], stdout=subprocess.PIPE)
    return subprocess.run(['grep', 'Core'], stdin=ps.stdout, stdout=subprocess.PIPE) \
        .stdout.decode('utf-8').splitlines()


def format_line(status: list) -> str:
    core_temps = ''
    for x in status:
        core_temps += re.search(r'\d+.\d+', x).group(0).replace('.0', '') + '\u00B0 ~ '
    return core_temps.strip(' ~ ')


if __name__ == "__main__":
    print(f' {format_line(get_cpu_status())}')
