#!/bin/bash

symlink() {
    printf "Symlinking '%s', to path '%s'\n" "repo/$1" "$HOME/$2"
    ln -s "$(realpath ./"$1")" "$HOME/$2"
}

symlink "betterlockscreen/betterlockscreenrc" ".config/betterlockscreenrc"

mkdir -p "$HOME/scripts/lock"
symlink "betterlockscreen/lock.py" "scripts/lock/lock.py"
symlink "betterlockscreen/lines" "scripts/lock/lines"

mkdir -p "$HOME/.config/i3blocks"
symlink "i3blocks/batt.py" ".config/i3blocks/batt.py"
symlink "i3blocks/mem.py" ".config/i3blocks/mem.py"
symlink "i3blocks/spotify.py" ".config/i3blocks/spotify.py"
symlink "i3blocks/volume.py" ".config/i3blocks/volume.py"
symlink "i3blocks/wifi.py" ".config/i3blocks/wifi.py"
symlink "i3blocks/cpu.py" ".config/i3blocks/cpu.py"
symlink "i3blocks/config" ".config/i3blocks/config"

mkdir -p "$HOME/.config/i3"
symlink "i3/config" ".config/i3/config"
