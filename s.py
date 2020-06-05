#!/bin/python3
import socket
import sys
import selectors

HOST = ''
PORT = 10000

count = 0

sel = selectors.DefaultSelector()

def accept(sock, mask):
    global count
    
    conn, addr = sock.accept()  # Should be ready
    count = count + 1
    print('Accepted from', addr)
    print('The number of connections is ' + str(count))
    
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    global count
    
    data = conn.recv(1000)  # Should be ready
    if data:
        print("Received:", repr(data))
        #print('echoing', repr(data), 'to', conn)
        #conn.send(data)  # Hope it won't block
    else:
        print('A connection is closing')
        count = count - 1
        print('The number of connections is ' + str(count))
        sel.unregister(conn)
        conn.close()

if len(sys.argv) > 1:
    port = PORT + int(sys.argv[1])
else:
    port = PORT
    
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, port))
sock.listen(10000)
sock.setblocking(False)

print("Listening:", port)

sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)                
