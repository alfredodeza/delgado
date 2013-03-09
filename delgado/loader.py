"""
JSON Loading utilities
"""
from json import loads
import delgado
from delgado.decorators import catches
from delgado.exceptions import Forbidden


@catches((ValueError, Forbidden))
def loader(string, allowed=None):
    allowed = allowed or delgado.config.get('allowed', [])
    obj = loads(string)
    for exe in obj.keys():
        if exe not in allowed:
            raise Forbidden('Executable %s, is not allowed' % exe)


def format_command(obj):
    executable = obj.keys()[0]
    arguments = obj[executable]
    return [executable] + arguments
