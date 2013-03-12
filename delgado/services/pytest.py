

class Pytest(object):

    help_menu = 'A handler for running py.test commands'


    def __init__(self, args):
        self.args = args
        print 'initing Pytest plugin'

    def parse_args(self):
        print 'parsing args'
