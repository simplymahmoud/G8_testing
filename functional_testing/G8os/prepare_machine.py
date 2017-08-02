#!/usr/bin/env python3
import g8core
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
target_ip = config['main']['target_ip']
print(target_ip)
client = g8core.Client(target_ip)
client.timeout = 100
client.btrfs.create('storage', ['/dev/sda'])
client.disk.mount('/dev/sda', '/var/cache', options=[""])

