from pytest import raises
from delgado import main


class TestMain(object):

    def test_get_help_with_no_args(self, capsys):
        with raises(SystemExit):
            main.Delgado([])
        out, err = capsys.readouterr()
        assert err == ''
        assert 'Version:' in out

    def test_load_pytest(self, capsys):
        main.Delgado(['delgado', '--log', 'debug'])
        out, err = capsys.readouterr()
        assert err == ''
        assert 'loading pytest' in out

    def test_info_logger_doesnt_show_plugin_loading(self, capsys):
        main.Delgado(['delgado', '--logging', 'info'])
        out, err = capsys.readouterr()
        assert 'loading pytest' not in out

    def test_unkown_command(self, capsys):
        main.Delgado(['delgado', '--foo', 'info'])
        out, err = capsys.readouterr()
        assert 'Unknown command' in out
