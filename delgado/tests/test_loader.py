from pytest import raises
from delgado import loader
from delgado.exceptions import InvalidFormat, Forbidden


class TestFormatCommand(object):

    def test_get_executable_first(self):
        obj = {'executable': [1, 2, 3]}
        result = loader.format_command(obj)
        assert result == ['executable', 1, 2, 3]

    def test_no_arguments_are_ok(self):
        obj = {'executable': []}
        result = loader.format_command(obj)
        assert result == ['executable']

    def test_raise_invalid_format(self):
        with raises(InvalidFormat):
            loader.format_command([])

    def test_get_correct_rpr(self):
        with raises(InvalidFormat) as exc:
            loader.format_command([])
        error = exc.value.args[0]
        assert 'received: []' in error

    def test_no_obj(self):
        with raises(InvalidFormat):
            loader.format_command({})


class TestLoader(object):

    def test_loader_simplest_obj(self):
        result = loader.loader("""{"foo": []}""", allowed=['foo'])
        assert result == ['foo']

    def test_loader_not_allowed(self):
        with raises(Forbidden):
            loader.loader("""{"foo": []}""")

    def test_unable_to_parse(self):
        with raises(InvalidFormat):
            loader.loader("""foo": []}""", allowed=['foo'])
