import socket
import os
from subprocess import call
from tambo import Transport
import delgado
from delgado.loader import loader
from delgado.exceptions import Forbidden, InvalidFormat, Reconnect
from delgado import logger


class Server(object):

    _help = """
Run the server that listens on a unix socket.

--allowed           The executable allowed to run for this listener
    """

    def __init__(self, argv):
        self.argv = argv

    def parse_args(self):
        options = ['--allowed']
        parser = Transport(self.argv, options=options)
        parser.catch_help = self._help
        parser.parse_args()
        delgado.config['allowed'] = parser.get('--allowed', [])
        self.run()

    def run(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.remove("/tmp/socketname")
        except OSError:
            pass
        try:
            while True:
                try:
                    s.bind("/tmp/socketname")
                    s.listen(1)
                    conn, addr = s.accept()
                except socket.error:
                    raise Reconnect
                while 1:
                    raw_data = conn.recv(1024)
                    try:
                        if not raw_data:
                            raise Reconnect
                        data = loader(raw_data)
                        logger.info("Running command: %s" % data)
                        call(data)
                    except (InvalidFormat, Forbidden) as error:
                        logger.error(error.message)
                        raise Reconnect
        except Reconnect:
            try:
                conn.close()
            except:
                pass
            self.run()
