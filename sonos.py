#!/usr/bin/env python3

import sys
import os.path
import _thread
import argparse
import requests
import readline
import netifaces
import ipaddress
import http.server

from soco import SoCo
from gtts import gTTS 
from datetime import datetime
from colorama import Fore, Style
from scapy.all import srp, Ether, ARP, conf

def print_cyan(line):
    print(Fore.CYAN + Style.BRIGHT + line +Fore.RESET + Style.NORMAL)

def print_green(line):
    print(Fore.GREEN + Style.BRIGHT + line + Fore.RESET + Style.NORMAL)

def print_red(line):
    print(Fore.RED + Style.BRIGHT + line + Fore.RESET + Style.NORMAL)

class TextToSpeech:

    def convert_text_to_speech(self, text, file_name):
        speech = gTTS(text=text, lang='en', slow=False) 
        speech.save(file_name)


class DeviceCompleter:

    def __init__(self, logic):
        self.logic = logic

    def traverse(self, tokens, tree):
        if tree is None:
            return []
        elif len(tokens) == 0:
            return []
        if len(tokens) == 1:
            return [x+' ' for x in tree if x.startswith(tokens[0])]
        else:
            if tokens[0] in tree.keys():
                return self.traverse(tokens[1:],tree[tokens[0]])
        return []

    def complete(self, text, state):
        try:
            tokens = readline.get_line_buffer().split()
            if not tokens or readline.get_line_buffer()[-1] == ' ':
                tokens += ['']
            results = self.traverse(tokens, self.logic) + [None]

            if state < len(results):
                return results[state]
            else:
                return None
        except Exception as e:
            print(e)

class SonoHunter:

    banner = '''--- SonoHunter ---\n'''

    def __init__(self, interface='wlan0'):
        self.connected_device = None
        self.translator = TextToSpeech()
        self.interface = interface

    def print_banner(self):
        print_cyan(self.banner)

    def print_help(self):
        print("\nAvailable commands:")
        print("\n - " + "\n - ".join(self.logic.keys()) + "\n")

    def get_wlan_ip(self):
        return netifaces.ifaddresses(self.interface)[netifaces.AF_INET][0]['addr']

    def connect(self, address):
        try:
            self.connected_device = SoCo(address)    
            self.connected_device.player_name
            print_green('Connection active')
        except ConnectionRefusedError:
            self.connected_device = None
            print_red('Connection Failed: connection refused to {}'.format(address))
        except OSError:
            self.connected_device = None
            print_red('Connection Failed: device {} not found'.format(address))
    
    def play_file(self, file_name):
        
        if self.connected_device is None:
            print_red('Not connected')
            return

        if not os.path.isfile(file_name):
            print_red('File not found')
            return

        port = 8080

        server = http.server.HTTPServer(('0.0.0.0', port), http.server.SimpleHTTPRequestHandler)
        print("Starting server")
        _thread.start_new_thread(server.handle_request, ()) 

        self.connected_device.play_uri('http://{}:{}/{}'.format(self.get_wlan_ip(), port, file_name))

        track = self.connected_device.get_current_track_info()

        print('playing {}'.format(track['title']))

        self.connected_device.play()

    def refresh_logic(self, devices):
        available_device_names = {dev['player_name']:None for dev in devices}
        available_device_names.update({dev['ip']:None for dev in devices})

        self.logic = {'help':None, 'say':None, 'volume':None, 'quit':None, 'stop':None, 'scan':None, 'connect':(available_device_names), 'play':{x:None for x in os.listdir() if os.path.isfile(x)}}

        readline.set_completer(DeviceCompleter(self.logic).complete)

    def print_active_devices(self):

        self.scan_active_devices()
        devices = self.active_devices

        print("Active devices found: ")
        if devices == []:
            print_red("None")
        else:
            for device in devices:
                print_green("{}: {}".format(device['player_name'], device['ip']))
            print()

    def scan_active_devices(self):

        print(" Hunting for devices ...\n")

        ifaddrs = netifaces.ifaddresses(self.interface)[netifaces.AF_INET][0]
        ips = str(ipaddress.IPv4Interface(ifaddrs['addr']+"/"+ifaddrs["netmask"]).network)

        start_time = datetime.now()

        conf.verb = 0
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ips), timeout=2, iface=self.interface, inter=0.01)

        sonos_macs = ["00:0E:58", "5C:AA:FD", "78:28:CA", "94:9F:3E", "B8:E9:37"]

        devices = [{'mac':recv.sprintf("%Ether.src%"), 'ip':recv.sprintf("%ARP.psrc%")} for sent, recv in ans]

        sonos_devices = []

        for device in devices:
            if (device['mac'][:8].upper() in sonos_macs):
                device['player_name'] = 'Error'
                try:
                    device['player_name'] = SoCo(device['ip']).player_name
                    sonos_devices.append(device)
                except e:
                    print(e)

        self.active_devices = sonos_devices
        self.refresh_logic(self.active_devices)

    def say(self, words):

        if self.connected_device is None:
            print_red('Not connected')
            return

        file_name = "words.mp3"

        try:
            self.translator.convert_text_to_speech(words, file_name)
        except:
            print_red("Error generating file")
            return

        try:
            self.play_file(file_name)
        except:
            print_red("Error sending speech")

    def process_command(self, command):
        """
        returns whether process should continue
        """
        command_parts = command.split(" ")

        if command_parts[0] in ['?', 'help']:
            self.print_help()
        elif command_parts[0] in ['stop', 'quit']:
            return False
        elif command_parts[0] == 'scan':
            self.print_active_devices()
        elif command_parts[0] == 'connect':
            ip = ''
            try:
                ipaddress.IPv4Address(command_parts[1])
                ip = command_parts[1]
            except ipaddress.AddressValueError:
                for dev in self.active_devices:
                    if command_parts[1] == dev['player_name']:
                        ip = dev['ip']
                        break
            try:
                self.connect(ip)
            except Exception as e:
                print_red('Error: {}'.format(e))
        elif command_parts[0] == 'volume':
            try:
                if self.connected_device is not None:       
                    self.connected_device.volume = command_parts[1]
            except Exception as e:
                print("Invalid value")
                
        elif command_parts[0] == 'play':
            try:
                if len(command_parts) > 1:
                    self.play_file(command_parts[1])
                else:
                    print("Invalid command")
            except Exception as e:
                print(e)
        elif command_parts[0] == 'say':
            try:
                if len(command_parts) > 1:
                    self.say(" ".join(command_parts[1:]))
                else:
                    print("Invalid command")
            except Exception as e:
                print(e)
        else:
            print("Command not found")

        return True   

    def command_loop(self, commands=None):

        readline.parse_and_bind('tab: complete')
        readline.parse_and_bind('set editing-mode emacs')

        try:
            self.print_banner()

            if commands is None or commands == []:
                self.print_active_devices()
            else:
                for comm in commands:
                    self.process_command(comm)

            should_continue = True
            while should_continue:
                should_continue = self.process_command(input('> '))

        except KeyboardInterrupt as e:
            pass
        except EOFError as e:
            print(Fore.RESET + Style.NORMAL)

        print_red("\nQuitting")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--interface', help='interface to use for scanning')
    parser.add_argument('-t','--target', help='ip to connect to (skip scan phase)')
    parser.add_argument('-f', '--file', help='file to play on device')


    if os.geteuid() != 0:
        exit("Needs to be run as root to do low level networking stuff")

    args = parser.parse_args()

    if args.interface is not None and args.interface not in netifaces.interfaces():
        exit("Specified interface {} not found".format(args.interface))

    sono_hunter = SonoHunter(interface=args.interface)

    commands = []

    if args.target is not None:
        commands.append('connect {}'.format(args.target))
        if args.file is not None:
            commands.append('play {}'.format(args.file))
    elif args.file:
        print('Cannot specify file without target device to play on')
        exit(0)

    sono_hunter.command_loop(commands)