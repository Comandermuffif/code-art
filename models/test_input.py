from io import StringIO

import shlex
import unittest

from models.input import InputEvaluator, InputParser, FunctionToken, ArrayToken, ValueToken


class InputParserUnitTests(unittest.TestCase):
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

    def test_standard(self):
        stream = StringIO("""SetColorMode(GradientColorMode([FFFFFF, 000000]))
SetDrawMode(VoronoiDrawMode(5000))
Draw()""")

        tokens = InputParser.parse(stream)
        self.assertEqual(3, len(tokens))

        if not isinstance(tokens[0], FunctionToken):
            self.fail("Expected function token")
        if not isinstance(tokens[1], FunctionToken):
            self.fail("Expected function token")
        if not isinstance(tokens[2], FunctionToken):
            self.fail("Expected function token")

        self.assertEqual(tokens[0].name, "SetColorMode")
        self.assertEqual(tokens[1].name, "SetDrawMode")
        self.assertEqual(tokens[2].name, "Draw")

        self.assertEqual(1, len(tokens[0].args))
        self.assertEqual(1, len(tokens[1].args))
        self.assertEqual(0, len(tokens[2].args))

        if not isinstance(tokens[0].args[0], FunctionToken):
            self.fail("Expected function token")
        if not isinstance(tokens[1].args[0], FunctionToken):
            self.fail("Expected function token")

        self.assertEqual("GradientColorMode", tokens[0].args[0].name)
        self.assertEqual("VoronoiDrawMode", tokens[1].args[0].name)

        self.assertEqual(1, len(tokens[0].args[0].args))
        self.assertEqual(1, len(tokens[1].args[0].args))

        if not isinstance(tokens[0].args[0].args[0], ArrayToken):
            self.fail("Expected function token")

        if not isinstance(tokens[0].args[0].args[0].items[0], ValueToken):
            self.fail("Expected value token")
        if not isinstance(tokens[0].args[0].args[0].items[1], ValueToken):
            self.fail("Expected function token")

        self.assertEqual("FFFFFF", tokens[0].args[0].args[0].items[0].value)
        self.assertEqual("000000", tokens[0].args[0].args[0].items[1].value)

        if not isinstance(tokens[1].args[0].args[0], ValueToken):
            self.fail("Expected function token")

        self.assertEqual("5000", tokens[1].args[0].args[0].value)


class InputEvaluatorUnitTests(unittest.TestCase):
    def test_add(self):
        stream = StringIO("test(add(1, 2))")
        tokens = InputParser.parse(stream)

        def test(input):
            self.assertEqual(3, input)

        evaluator = InputEvaluator([test])
        evaluator.parse(tokens)

    def test_sub(self):
        stream = StringIO("test(sub(1, 2))")
        tokens = InputParser.parse(stream)

        def test(input):
            self.assertEqual(-1, input)

        evaluator = InputEvaluator([test])
        evaluator.parse(tokens)

    def test_mult(self):
        stream = StringIO("test(mult(3, 2))")
        tokens = InputParser.parse(stream)

        def test(input):
            self.assertEqual(6, input)

        evaluator = InputEvaluator([test])
        evaluator.parse(tokens)

    def test_div(self):
        stream = StringIO("test(div(1, 2))")
        tokens = InputParser.parse(stream)

        def test(input):
            self.assertEqual(0.5, input)

        evaluator = InputEvaluator([test])
        evaluator.parse(tokens)

    def test_sum(self):
        stream = StringIO("test(sum([1, 2]))")
        tokens = InputParser.parse(stream)

        def test(input):
            self.assertEqual(3, input)

        evaluator = InputEvaluator([test])
        evaluator.parse(tokens)