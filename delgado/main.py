import sys
from tambo import Transport
import delgado
from delgado.server import Server
from delgado.decorators import catches


class Delgado(object):
    _help = """
delgado: A utility to run in the foreground and listen for commands
to execute frmo the network to the terminal
descriptive tests.

Global Options:
--log, --logging    Set the level of logging. Acceptable values:
                    debug, warning, error, critical

run                 Run the server, listening on a unix socket.

Version: %s

    """ % delgado.__version__

    mapper = {'run': Server}

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

    @catches(KeyboardInterrupt)
    def main(self, argv):
        options = [['--log', '--logging']]
        self.config = {}

        parser = Transport(argv, mapper=self.mapper,
                           options=options, check_help=False,
                           check_version=False)
        parser.catch_help = self._help
        parser.catch_version = delgado.__version__
        parser.parse_args()
        delgado.config = {'verbosity': parser.get('--log', 'debug')}

        if len(argv) <= 1:
            return parser.print_help()
        parser.dispatch()
        parser.catches_help()
        parser.catches_version()
