#!/bin/bash

symlink() {
    printf "Symlinking '%s', to path '%s'\n" "repo/$1" "$HOME/$2"
    ln -s "$(realpath ./"$1")" "$HOME/$2"
}

sys_symlink() {
    printf "Symlinking '%s', to path '%s'\n" "repo/$1" "$2"
    # require sudo for file system symlinks
    sudo ln -s "$(realpath ./"$1")" "$2"
}

# initial necessities
# needs manual install
# sudo pacman -S base-devel sudo vim netctl wpa_supplicant dialog

# basic desktop
echo 'setting up basic desktop'
sudo pacman -S i3-gaps i3blocks i3status xorg-server lightdm lightdm-gtk-greeter konsole

# utility
# ntfs-3g: allow write on usb drives
sudo pacman -S ntfs-3g

# yay
wget https://aur.archlinux.org/cgit/aur.git/snapshot/yay.tar.gz
mkdir build
mv yay.tar.gz build
cd build
tar -xvf yay.tar.gz
cd yay
makepkg -si
cd

# enable multilib
sudo sed -i "s/#[multilib]/[multilib]/g" /etc/pacman.conf
sudo sed -i "s/#Include = /etc/pacman.d/mirrorlist/Include = /etc/pacman.d/mirrorlist/g" /etc/pacman.conf

# install remaining
# xclip: clipboard utility for i3 binds
# upower: utility for battery block in i3
yay -S spotirec-git chwifi-git escrotum-git pycharm-community-edition xclip wine \
       whatsapp-nativefier vlc upower typora ttf-dejavu ttf-hanazono ttf-liberation trello \
       tixati steam-fonts steam spotify spicetify-cli smartmontools slack-desktop rofi pulseaudio
       playerctl parole p7zip obs-studio noto-fonts noto-fonts-emoji nmap neofetch nemo lutris
       inkscape htop gimp freetype2 firefox feh evince dunst drun docker discord cloc caprine
       calibre blender betterlockscreen arc-gtk-theme-git \

# todo
# usb drive:
#   wp dir to /home/usr/wp


symlink "betterlockscreen/betterlockscreenrc" ".config/betterlockscreenrc"

mkdir -p "$HOME/scripts/lock"
symlink "betterlockscreen/lock.py" "scripts/lock/lock.py"
symlink "betterlockscreen/lines" "scripts/lock/lines"

symlink "monitor/monitor.py" "scripts/monitor.py"

mkdir -p "$HOME/.config/i3blocks"
symlink "i3blocks/batt.py" ".config/i3blocks/batt.py"
symlink "i3blocks/mem.py" ".config/i3blocks/mem.py"
symlink "i3blocks/spotify.py" ".config/i3blocks/spotify.py"
symlink "i3blocks/volume.py" ".config/i3blocks/volume.py"
symlink "i3blocks/disk.py" ".config/i3blocks/disk.py"
symlink "i3blocks/wifi.py" ".config/i3blocks/wifi.py"
symlink "i3blocks/cpu.py" ".config/i3blocks/cpu.py"
symlink "i3blocks/load.py" ".config/i3blocks/load.py"
mkdir -p "$HOME/.config/i3blocks/dmi-weather"
symlink "i3blocks/dmi-weather/weather.py" ".config/i3blocks/dmi-weather/weather.py"
symlink "i3blocks/dmi-weather/cities" ".config/i3blocks/dmi-weather/cities"
symlink "i3blocks/config" ".config/i3blocks/config"

mkdir -p "$HOME/.config/i3"
symlink "i3/config" ".config/i3/config"

mkdir -p "$HOME/.config/dunst"
symlink "dunst/dunstrc" ".config/dunst/dunstrc"

sys_symlink "shufflewall/shufflewall.service" "/etc/systemd/system/shufflewall.service"
sys_symlink "shufflewall/shufflewall.timer" "/etc/systemd/system/shufflewall.timer"
