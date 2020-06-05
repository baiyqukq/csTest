#!/bin/python

import socket
import sys
import time

HOST, PORT = "127.0.0.1", 10000

socks = []

def new_connection(port):
    global socks
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
       sock.connect((HOST, port))
    except OSError as msg:
        print("Failed to connect")
        return False
        
    sock.sendall(b'Hello World')
    socks.append(sock)
    return True

if __name__ == "__main__":
    print("Begin")

    for i in range(10):
        for j in range(500):
            if not new_connection(PORT + i):
                print("Stopped")
                break

    print("Done")
    time.sleep(5)

    for sock in socks:
        sock.close()
