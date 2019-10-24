# sonos_hunter
Connect and play with sonos speakers


## Starting up

when starting with no arguments the program will start by scanning for available devices

if you specify a device ip with **-t** or **--target** it will skip scanning and connect straight away

if you specify a target you can also specify a file to play immediately with **-f** as well

you can specify a partiular interface with the **-i** or **--interface** option

## Usage

```
usage: sonos.py [-h] [-i INTERFACE] [-t TARGET] [-f FILE]

optional arguments:
  -h, --help            show this help message and exit
  -i, --interface INTERFACE
                        interface to use for scanning
  -t, --target TARGET
                        ip to connect to (skip scan phase)
  -f, --file FILE  file to play on device

```

## Commands

help: displays a help menu

scan: scans for devices

volume: change volume of connected device (0 - 100)

play: play a given audio file

say: convert text to speech and play on speaker, uses google api so need to be online

connect: connect to a device, can either specify using a speaker name or ip address

stop, quit: quit cli


