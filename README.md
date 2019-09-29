# sonos_hunter
Connect and play with sonos speakers


## Starting up

when starting with no arguments the program will start by scanning for available devices

if you specify a device ip with -t or --target it will skip scanning and connect straight away

if you specify a target you can also specify a file to play immediately with -f as well

## Commands

help: displays a help menu

scan: scans for devices

volume: change volume of connected device (0 - 100)

play: play a given audio file

say: convert text to speech and play on speaker, uses google api so need to be online

connect: connect to a device, can either specify using a speaker name or ip address

stop, quit: quit cli


