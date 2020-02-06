#!/usr/bin/env python
import os


def print_result(load, color):
    os.system(f'echo " {load}"')
    os.system(f'echo ')
    os.system(f'echo "{color}"')


def get_load_status() -> list:
    with open('/proc/loadavg', 'r') as f:
        return f.read().strip('\n').split(' ')


def print_line(status: list):
    # [1 min, 5 min, 10 min]
    if float(status[0]) > 5.0:
        if float(status[0]) > 10.0:
            print_result(load=status[0], color='#FA5858')
        else:
            print_result(load=status[0], color='#F4FA58')
    else:
        print(f' {status[0]}')


if __name__ == "__main__":
    print_line(get_load_status())
