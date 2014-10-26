import socket
import threading
import SocketServer
import sys
import random
import re
import sys
import time

def fib():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

def get_fib_number(num):
    for index, curr_fib in enumerate(fib()):
        if index == int(num)-1:
            return curr_fib

def client(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        response = sock.recv(1024)
        print response.replace('\n', '')
        print 'HELLO'
        sock.sendall('HELLO')
        while True:
            try:
                response = sock.recv(1024)
                # print "CLIENT RECV: {}".format(response)
                if response:
                    print response
                if "flag{" in response:
                    break
                match = re.search("What is the ([0-9]+) number", response)
                curr_answer = str(get_fib_number(match.group(1)))
                sock.sendall(curr_answer)
                # print "CLIENT SEND: {}".format(curr_answer)
                response = ''
            except Exception as e:
                pass
    finally:
        sock.close()

if __name__ == '__main__':
    client('127.0.0.1', int(sys.argv[1]))
