#!/usr/bin/env python
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


# Funtion to print the output in the desired manner.
def format_line(data):
    return (("%(time)5s: New connection: %(local)15s -> %(remote)15s" % data) + "\n")

 # List to collect connection samples 
connection_samplings = []

# Dict to create a key pair for local and remote IPs
remote_ip_local_ip_mapping = {}

# Main function to read /proc/net/tcp file and print the output every 10 seconds
def main():
    rv = []
    with open('/proc/net/tcp') as f:
        sockets = process_file(f.read())
    current_time_connections = []
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
            remote_ip_local_ip_mapping[convert_linux_netaddr(_[2]).split(":")[0]] = convert_linux_netaddr(_[1]).split(":")[0]
            current_time_connections.append(convert_linux_netaddr(_[2]))
            rv.append(_tmp)
    connection_samplings.append(current_time_connections)
    print_connections_within_lastMinute(3)
    if len(rv) > 0:
        for _ in rv:
            sys.stdout.write(format_line(_))

# Function for port scanning and printing
def print_connections_within_lastMinute(atleast_connections_times):
    if len(connection_samplings) > 6:
        ip_count_map = {}
        # sliding window - get the last 6 sampling connections with a sampling rate of 10sec
        temp1 = connection_samplings[: -6]
        # move the window to last 5 sampling connections
        temp2 = connection_samplings[1:]
        for connections in temp1:
            for connection in connections:
                ip_port = connection.split(":")
                ip = ip_port[0]
                port = ip_port[1]
                if ip not in ip_count_map.keys():
                    ip_count_map[ip] = set()
                ip_count_map[ip].add(port)

        # print the connections with at least connected as atleast_connections_times
        for ip in ip_count_map.keys():
            if len(ip_count_map[ip]) >= atleast_connections_times:
                sys.stdout.write(ip + " -> " + remote_ip_local_ip_mapping[ip] + " ports - " + ','.join(ip_count_map[ip])+ "\n")

        del connection_samplings[:]
        for connections in temp2:
            connection_samplings.append(connections)


# scheduler to run the program every 10 seconds
schedule.every(10).seconds.do(main)
while 1:
    schedule.run_pending()
    # To make sure that the script doesn't hog all the CPU usage
    time.sleep(1)
