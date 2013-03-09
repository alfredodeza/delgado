import sys
from tambo import Transport
import delgado
from delgado.server import Server


class Delgado(object):
    _help = """
delgado: A utility to run in the foreground and listen for commands
to execute frmo the network to the terminal
descriptive tests.

run         Run the server, listening on a unix socket.

Version: %s

    """ % delgado.__version__

    def __init__(self, argv=None, parse=True):
        if argv is None:
            argv = sys.argv
        if parse:
            self.main(argv)

    def msg(self, msg, stdout=True):
        if stdout:
            sys.stdout.write(msg + '\n')
        else:
            sys.stderr.write(msg + '\n')
        sys.exit(1)

    def main(self, argv):
        options = []
        self.config = {}

        parser = Transport(argv, options=options)
        parser.catch_help = self._help
        parser.parse_args()
        parser.mapper = {'run': Server}

        if not parser.items():
            return parser.print_help()

        try:
            parser.dispatch()
        except KeyboardInterrupt:
            self.msg("Exiting from delgado.")
