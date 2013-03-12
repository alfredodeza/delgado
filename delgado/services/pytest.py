from tambo import Transport
import delgado
from delgado.server import Engine


class Pytest(object):

    help_menu = 'A handler for running py.test commands'
    _help = """
Run a base socket listener that allows py.test commands.

--socket-location   The location for the socket (defaults
                    to /tmp/pytest.sock)
    """

    def __init__(self, argv):
        self.argv = argv

    def parse_args(self):
        parser = Transport(self.argv, options=['--socket-location'])
        parser.catch_help = self._help
        parser.parse_args()
        location = parser.get('--socket-location', '/tmp/pytest.sock')
        delgado.config['allowed'] = ['py.test']
        engine = Engine(socket_location=location)
        engine.run_forever()
