#! /bin/bash
max_value=`awk '{print $1}' /sys/class/backlight/intel_backlight/max_brightness`
set_value=`echo $1 | awk '{print int($1)}'`

sum=$((set_value * 100 / max_value ))

#echo $sum
xbacklight -set $sum

exit 0
