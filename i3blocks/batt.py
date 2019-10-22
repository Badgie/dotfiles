#!/usr/bin/env python

import subprocess
import re
import os


def print_result(charge, color):
    os.system(f'echo " {charge}%"')
    os.system(f'echo ')
    os.system(f'echo "{color}"')


def get_battery_status() -> list:
    ps = subprocess.Popen(['upower', '-i', '/org/freedesktop/UPower/devices/battery_BAT0'], stdout=subprocess.PIPE)
    status = subprocess.run(['grep', 'energy'], stdin=ps.stdout, stdout=subprocess.PIPE).stdout.decode('utf-8')
    return re.split('\n', status)


def print_line(status: list):
    regex = r'\d+\.\d+'
    # [energy, energy-empty, energy-full, energy-full-design, energy-rate]
    try:
        current_charge = round(
            float(re.search(regex, status[0]).group(0)) / float(re.search(regex, status[2]).group(0)) * 100,
            2)
        if current_charge < 50:
            if current_charge < 20:
                print_result(charge=current_charge, color='#FA5858')
            else:
                print_result(charge=current_charge, color='#F4FA58')
        else:
            print(f' {current_charge}%')
    except:
        print(f' \u2620')


if __name__ == "__main__":
    print_line(get_battery_status())
