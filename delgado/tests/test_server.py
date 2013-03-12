from mock import Mock
from pytest import raises
from delgado import server


class TestServer(object):

    def setup(self):
        self.conn = Mock()
        self.conn.return_value = self.conn

    def set_debug_level(self):
        import delgado
        delgado.config['verbosity'] = 'debug'

    def test_run(self):
        # meh just excercising code really
        fake_conn = Mock(side_effect=TypeError)
        srv = server.Server([], connection=fake_conn)
        with raises(TypeError):
            srv.parse_args()

    def test_not_allowed(self, capsys):
        self.set_debug_level()
        self.conn.recv = Mock(side_effect=["""{"ls": []}""", TypeError])
        srv = server.Server([], connection=self.conn)
        with raises(TypeError):
            srv.parse_args()
        out, err = capsys.readouterr()
        assert 'ls, is not allow' in out
