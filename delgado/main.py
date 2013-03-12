import pkg_resources
import sys

from tambo import Transport
from delgado import logger
import delgado
from delgado.server import Server
from delgado.decorators import catches


class Delgado(object):
    _help = """
delgado: A utility to run in the foreground and listen for commands
to execute from the network to the terminal
descriptive tests.
Version: %s

Global Options:
--log, --logging    Set the level of logging. Acceptable values:
                    debug, warning, error, critical

run                 Run the server, listening on a unix socket.


Plugins:
%s

    """

    mapper = {'run': Server}

    def __init__(self, argv=None, parse=True):
        self.plugin_help = "No plugins found/loaded"
        if argv is None:
            argv = sys.argv
        if parse:
            self.main(argv)

    def help(self):
        return self._help % (delgado.__version__, self.plugin_help)

    def enable_plugins(self):
        """
        Load all plugins available, add them to the mapper and extend the help
        string with the information from each one
        """
        plugins = _load_library_extensions()
        for plugin in plugins:
            self.mapper[plugin._delgado_name_] = plugin
        self.plugin_help = ''.join(['%-19s %s' % (
            plugin._delgado_name_, getattr(plugin, 'help_menu', ''))
            for plugin in plugins])

    @catches(KeyboardInterrupt)
    def main(self, argv):
        options = [['--log', '--logging']]
        parser = Transport(argv, mapper=self.mapper,
                           options=options, check_help=False,
                           check_version=False)
        parser.parse_args()
        delgado.config['verbosity'] = parser.get('--log', 'info')
        self.enable_plugins()
        parser.catch_help = self.help()
        parser.catch_version = delgado.__version__
        parser.mapper = self.mapper
        if len(argv) <= 1:
            return parser.print_help()
        parser.dispatch()
        parser.catches_help()
        parser.catches_version()


def _load_library_extensions():
    """
    Locate all setuptools entry points by the name 'delgado_handlers'
    and initialize them.
    Any third-party library may register an entry point by adding the
    following to their setup.py::

        entry_points = {
            'delgado_handlers': [
                'plugin_name = mylib.mymodule:Handler_Class',
            ],
        },

    `plugin_name` will be used to load it as a sub command.
    """
    group = 'delgado_handlers'
    entry_points = pkg_resources.iter_entry_points(group=group)
    plugins = []
    for ep in entry_points:
        try:
            logger.debug('loading %s' % ep.name)
            plugin = ep.load()
            plugin._delgado_name_ = ep.name
            plugins.append(plugin)
        except Exception as error:
            logger.error("Error initializing plugin %s: %s" % (ep, error))
    return plugins



