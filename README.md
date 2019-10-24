# sonos_hunter
Connect and play with sonos speakers

## Starting up

When starting with no arguments the program will start by scanning for available devices

<<<<<<< HEAD
If you specify a device ip with -t or --target it will skip scanning and connect straight away

If you specify a target you can also specify a file to play immediately with -f as well
=======
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
>>>>>>> master

## Commands

<kbd>help</kbd>: displays a help menu

<kbd>scan</kbd>: scans for devices

<kbd>volume</kbd>: change volume of connected device (0 - 100)

<kbd>play</kbd>: play a given audio file

<kbd>say</kbd>: convert text to speech and play on speaker, uses google api so need to be online

<kbd>connect</kbd>: connect to a device, can either specify using a speaker name or ip address

<kbd>stop</kbd>, <kbd>quit</kbd>: quit cli

## Running With Docker :whale:
To run the following application as a docker container follow the following steps to access the cli.
1. ```docker build -t sonos-hunter .```
2. ```docker run sonos-hunter```
   - Alternatively you can run the container in detached mode (run container in background) 
   - ```docker run -d sonos-hunter```
  
*I will eventually just push something to dockerhub  that can be pulled and run*