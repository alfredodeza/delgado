import sys
from tambo import Transport
from delgado.server import Server

__version__ = '0.0.1'


class Commands(object):
    _help = """
delgado: A utility to run in the foreground and listen for commands
to execute frmo the network to the terminal
descriptive tests.

Version: %s

    """ % __version__

    def __init__(self, argv=None, parse=True):
        if argv is None:
            argv = sys.argv
        if parse:
            self.main(argv)

    def msg(self, msg, stdout=True):
        if stdout:
            sys.stdout.write(msg+'\n')
        else:
            sys.stderr.write(msg+'\n')
        sys.exit(1)

    def main(self, argv):
        options = []
        self.config = {}

        parser = Transport(argv, options=options)
        parser.catch_help = self._help
        parser.parse_args()
        parser.mapper = { 'run' : Server }

        try:
            parser.dispatch()
            print 'some foo'
        except KeyboardInterrupt:
            self.msg("Exiting from delgado.")
