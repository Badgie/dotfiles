import argparse
import os

parser = argparse.ArgumentParser(prog='')
parser.add_argument('--work', action='store_true', help='switch to work setup')
parser.add_argument('--home', action='store_true', help='switch to home setup')


def work():
    os.system('xrandr --output VGA1 --above LVDS1')
    update_lock()
    exit(0)


def home():
    os.system('xrandr --output VGA1 --off')
    update_lock()
    exit(0)


def update_lock():
    os.system('betterlockscreen -u ~/scripts/lock/wp/')


if __name__ == '__main__':
    args = parser.parse_args()
    if args.work:
        work()
    elif args.home:
        home()
    parser.print_help()
    exit(1)
