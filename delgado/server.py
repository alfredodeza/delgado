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
        engine = Engine()
        engine.run_forever()


class Engine(object):

    def __init__(self, socket_location=None, connection=None):
        self.socket_location = socket_location or '/tmp/delgado.sock'
        self.connection = connection or self.make_connection()

    def run_forever(self):
        while True:
            try:
                logger.debug('creating a new connection')
                self.run()
            except Reconnect:
                pass

    def make_connection(self):
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            os.remove(self.socket_location)
        except OSError:
            pass
        s.bind(self.socket_location)
        s.listen(1)
        conn, addr = s.accept()
        logger.debug('connection ready and listenting')
        return conn

    def run(self):
        conn = self.connection()
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
        finally:
            conn.close()
            logger.debug('connection closed')
