#!/usr/bin/env python
# importing required packages
import datetime
import re
import sys
import schedule
import time

# Function to process the input file


def process_file(procnet):
    sockets = procnet.split('\n')[1:-1]
    return [line.strip() for line in sockets]

# Function to split the hex IP address into chunks of two for easy conversion


def split_every_n(data, n):
    return [data[i:i + n] for i in range(0, len(data), n)]

# Function to convert the hex IP address and Port into decimal format


def convert_linux_netaddr(address):
    hex_addr, hex_port = address.split(':')

    addr_list = split_every_n(hex_addr, 2)
    addr_list.reverse()

    addr = ".".join(map(lambda x: str(int(x, 16)), addr_list))
    port = str(int(hex_port, 16))

    return "{}:{}".format(addr, port)

# Funtion to print the output in the desired manner


def format_line(data):
    return (("%(time)5s: New connection: %(local)15s \
    -> %(remote)15s" % data) + "\n")

# Main function to read file and print the output every 10 seconds


def main():
    rv = []
    with open('/proc/net/tcp') as f:
        sockets = process_file(f.read())
    for info in sockets:
        _ = re.split(r'\s+', info)
        now = datetime.datetime.now()
        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
        if len(_) > 1 and _[3] == '06':
            _tmp = {
                'time': formatted_time,
                'local': convert_linux_netaddr(_[1]),
                'remote': convert_linux_netaddr(_[2]),
            }
            rv.append(_tmp)
    if len(rv) > 0:
        for _ in rv:
            sys.stdout.write(format_line(_))

# scheduler to run the program every 10 seconds


schedule.every(10).seconds.do(main)
while 1:
    schedule.run_pending()
# To make sure that the script doesn't hog all the CPU usage
    time.sleep(1)
