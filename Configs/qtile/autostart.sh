#! /bin/fish

# Wallpaper
nitrogen --restore &
#urxvtd -q -o -f &

# Set Trackpad
xinput set-prop "ETPS/2 Elantech Touchpad" "libinput Tapping Enabled" 1
sleep 2;
xinput set-prop "ETPS/2 Elantech Touchpad" "libinput Natural Scrolling Enabled" 1

# Wifi
wicd-client -t &

# Bluetooth
blueberry-tray &
