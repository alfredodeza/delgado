import socket
import os


class Server(object):

    def __init__(self, argv):
        self.argv = argv

    def parse_args(self):
        self.run()

    def run(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.remove("/tmp/socketname")
        except OSError:
            pass
        s.bind("/tmp/socketname")
        while True:
            s.listen(1)
            conn, addr = s.accept()
            while 1:
                data = conn.recv(1024)
                if not data:
                    break
                print data
                from subprocess import call

                call(data.split())
        conn.close()
