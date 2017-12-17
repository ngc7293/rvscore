#!/usr/bin/python3
# -*- coding: utf-8 -*- 
""" Read RVGL time files """
from pathlib import Path
import os
import json
import requests

URL = 'http://127.0.0.1:8000/sync'
ROOT_FOLDER = '/usr/share/games/rvgl/times'
RV_HDR = b'\x02\x19\x00\x00\x86\x2c\x00\x00\x9c\x4d\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
RV_PAD = b'\x40\x77\x1b\x00\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x00\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x2d\x00'

def main():
    data = {}
    walk_read(Path(ROOT_FOLDER), data)
    datajson = json.dumps(data)

    # Push new times
    r = requests.post(URL, datajson);
    if r.status_code == 200:
        print('[PUSH] {} new times'.format(r.text))
    else:
        print("[PUSH] Err {}".format(r.status_code))

    # Get new times
    r = requests.get(URL)
    if r.status_code == 200:
        num = walk_write(json.loads(r.text))
        print('[PULL] {} new times'.format(num))
    else:
        print("[PULL] Err {}".format(r.status_code))


def walk_read(root, data):
    """ Walk filesystem (starting at root) to build times dict """
    empty = True
    for path in root.iterdir():
        # Navigate subdir
        if path.is_dir():
            data[path.name] = {}
            if walk_read(path, data[path.name]):
                data.pop(path.name)
            else:
                empty = False

        # Read time files
        if path.is_file() and path.suffix == '.times':
            name = path.name.split('.')[0]
            data[name] = read_times_file(path)
            if not data[name]:
                data.pop(name)
            else:
                empty = False
    return empty


def read_times_file(file):
    """
        Read a RVGL .times file and return a list of times. Only returns valid
        times. Each element of the list a dict with the keys 'time' (in ms),
        'profile' (str) and 'car' (str).
    """
    times = []
    with open(file, 'rb') as f:

        # Skip first line (no data for some reason)
        buf = bytes(f.read(40))

        buf = bytes(f.read(40))
        while len(buf) == 40:
            time = {}
            time['time'] = buf[0] | (buf[1] << 8) | (buf[2] << 16) | (buf[3] << 24);
            time['profile'] = str(buf[4:20], 'ascii').rstrip('\0')
            time['car'] = str(buf[20:40], 'ascii').rstrip('\0')

            if time['time'] != 1800000:
                times.append(time)

            buf = bytes(f.read(40))
    return times


def walk_write(data):
    new = 0
    for mode in data:
        for category in data[mode]:
            for track in data[mode][category]:
                new += write_times_file(data[mode][category][track], "{}/{}/{}/{}.times".format(ROOT_FOLDER, mode, category, track))
    return new

def write_times_file(synctimes, file):
    if os.path.exists(file):
        times = read_times_file(file)
        for i, synctime in enumerate(synctimes):
            for time in times:
                if synctime == time:
                    synctimes.pop(i)
        if not synctimes:
            return 0
        times = (synctimes + times)[:10]
    else:
        times = synctimes[:10]

    with open(file, 'wb') as f:
        f.write(RV_HDR)
        for time in times:
            f.write(time_to_hex(time))
        for i in range(0, 10 - len(time)):
            f.write(RV_PAD)

    return len(synctimes)

def time_to_hex(time):
    s = b''
    s += time['time'].to_bytes(4, byteorder='little', signed=True)
    s += str(time['profile'] + '\0' * (16 - len(time['profile']))).encode('ascii')
    s += str(time['car'] + '\0' * (20 - len(time['car']))).encode('ascii')
    return s

if __name__ == '__main__':
    main()

