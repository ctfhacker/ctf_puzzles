import socket
import threading
import SocketServer
import sys
import random
import re

FLAG = "are't_sockets_funs"

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def setup(self):
        self.request.settimeout(1)

    def _fib(self):
        a, b = 0, 1
        while True:
            yield a
            a, b = b, a + b

    def _get_fib_number(self, num):
        for index, curr_fib in enumerate(self._fib()):
            if index == num-1:
                return curr_fib

    def _generate_question(self):
        num = random.randint(40, 200)
        question = "What is the {} number in the fibonacci sequence?\n".format(num)
        answer = self._get_fib_number(num)
        # print "Returning {} {}".format(question, answer)
        return (question, answer)

    def _close_socket(self, message):
        self.request.sendall(message + "\n")
        self.server.shutdown_request(self.request)
        self.server.close_request(self.request)
    
    def handle(self):
        keyword = 'HELLO'
        quiz_length = 25
        initial_question = 'Enter {} to continue\n'.format(keyword)
        quiz_banner = """
Welcome to the FIBQUIZ!
Answer the following questions in the time allowed for the flag.
For reference:
1st - 0
2nd - 1
3rd - 1
ect...
Must answer {} in a row correctly!\n\n
""".format(quiz_length)
          
        try:
            self.request.sendall(initial_question)
            data = self.request.recv(1024)
            if keyword not in data:
                self._close_socket("Wrong response.")
                return

            correct_answers = 0
            question, answer = self._generate_question()
            self.request.sendall(quiz_banner + question)

            while correct_answers < quiz_length:
                data = self.request.recv(1024)
                # print "SERVER RECV: {}".format(data)
                if int(data) != answer:
                    self._close_socket("You were soo close..")
                    return

                correct_answers = correct_answers + 1
                if correct_answers == quiz_length:
                    self.request.sendall("Congratz!\n")
                    self.request.sendall("flag({})\n".format(FLAG))
                    self._close_socket("Hope you had fun!")
                    return
                
                question, answer = self._generate_question()
                self.request.sendall(question)

        except Exception as e:
            if 'timed out' in str(e):
                self.request.sendall("FAIL: Type faster young grasshopper\nTry again.\n")

    def handle_timeout(self):
        self.request.sendline("Thread timeout")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", int(sys.argv[1])

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)

    # server_thread.daemon = False
    server_thread.timeout = 1
    server_thread.start()
