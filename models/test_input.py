import shlex
import unittest

from models.input import InputParser, FunctionToken, ArrayToken, ValueToken


class ParsingUnitTests(unittest.TestCase):
    def test_value(self):
        reader = shlex.shlex("item1")
        valueToken = InputParser._parseToken(reader)

        if not isinstance(valueToken, ValueToken):
            self.fail("Did not get a value token")

        self.assertEqual("item1", valueToken.value)

    def test_array(self):
        reader = shlex.shlex("[item1, item2]")
        arrayToken = InputParser._parseToken(reader)

        if not isinstance(arrayToken, ArrayToken):
            self.fail("Did not get an array token")

        self.assertEqual(2, len(arrayToken.items))

        if not isinstance(arrayToken.items[0], ValueToken):
            self.fail("Array item 0 is not a value token")

        self.assertEqual("item1", arrayToken.items[0].value)

        if not isinstance(arrayToken.items[1], ValueToken):
            self.fail("Array item 1 is not a value token")

        self.assertEqual("item2", arrayToken.items[1].value)

    def test_function(self):
        reader = shlex.shlex("SetColorMode(arg1, arg2)")
        funcToken = InputParser._parseToken(reader)

        if not isinstance(funcToken, FunctionToken):
            self.fail("Did not get a function token")

        self.assertEqual("SetColorMode", funcToken.name)

        self.assertEqual(2, len(funcToken.args))

        if not isinstance(funcToken.args[0], ValueToken):
            self.fail("Arg 0 is not a value token")

        if not isinstance(funcToken.args[1], ValueToken):
            self.fail("Arg 1 is not a value token")

        self.assertEqual("arg1", funcToken.args[0].value)
        self.assertEqual("arg2", funcToken.args[1].value)