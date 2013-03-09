from pytest import raises
from delgado import loader


class TestFormatCommand(object):

    def test_get_executable_first(self):
        obj = {'executable': [1, 2, 3]}
        result = loader.format_command(obj)
        assert result == ['executable', 1, 2, 3]

    def test_no_arguments_are_ok(self):
        obj = {'executable': []}
        result = loader.format_command(obj)
        assert result == ['executable']

    def test_raise_invalid_format(self, capsys):
        with raises(SystemExit):
            loader.format_command([])
        out, err = capsys.readouterr()
        assert 'InvalidFormat' in err

    def test_get_correct_rpr(self, capsys):
        with raises(SystemExit):
            loader.format_command([])
        out, err = capsys.readouterr()
        assert 'received: []' in err
