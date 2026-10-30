from io import StringIO

import shlex
import unittest

from models.input import InputError, InputEvaluator, InputParser, ParseError, FunctionToken, ArrayToken, ValueToken


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


class ParseErrorUnitTests(unittest.TestCase):
    def assertParseError(self, source, line, column, *fragments):
        with self.assertRaises(ParseError) as context:
            InputParser.parse(StringIO(source))

        error = context.exception
        self.assertEqual(line, error.line)
        self.assertEqual(column, error.column)
        for fragment in fragments:
            self.assertIn(fragment, str(error))
        return error

    def test_unterminated_array_points_at_opening_bracket(self):
        self.assertParseError("Draw([1, 2", 1, 6, "unterminated array", "expected ']'")

    def test_unterminated_array_on_later_line(self):
        self.assertParseError("Draw()\nSetFoo([1", 2, 8, "unterminated array")

    def test_unterminated_argument_list_names_the_function(self):
        self.assertParseError(
            "SetColorMode(GradientColorMode([FFFFFF, 000000])\nDraw()",
            1, 13,
            "unterminated argument list to 'SetColorMode'",
            "expected ')'",
        )

    def test_mismatched_closer_points_at_both_ends(self):
        self.assertParseError(
            "Draw([1, 2)", 1, 11,
            "unexpected ')'",
            "expected ']'",
            "opened at line 1, column 6",
        )

    def test_stray_closer_at_top_level(self):
        self.assertParseError("Draw()\n]", 2, 1, "unexpected ']'", "nothing is open")

    def test_stray_opening_paren(self):
        self.assertParseError("(Draw)", 1, 1, "unexpected '('")

    def test_unterminated_quotation(self):
        self.assertParseError('Draw("abc)', 1, None, "No closing quotation")

    def test_error_snippet_shows_the_failing_line(self):
        error = self.assertParseError("Draw([1, 2", 1, 6, "unterminated array")
        self.assertIn("\n  Draw([1, 2\n" + " " * 7 + "^", str(error))


class TokenPositionUnitTests(unittest.TestCase):
    def test_tokens_carry_their_source_position(self):
        source = "SetColorMode([FFFFFF, 000000])\nDraw()"
        tokens = InputParser.parse(StringIO(source))

        self.assertEqual((1, 1), (tokens[0].line, tokens[0].column))
        self.assertEqual((1, 14), (tokens[0].args[0].line, tokens[0].args[0].column))
        self.assertEqual((1, 15), (tokens[0].args[0].items[0].line, tokens[0].args[0].items[0].column))
        self.assertEqual((1, 23), (tokens[0].args[0].items[1].line, tokens[0].args[0].items[1].column))
        self.assertEqual((2, 1), (tokens[1].line, tokens[1].column))
        self.assertEqual(source, tokens[0].source)

    def test_quoted_value_position_points_at_the_quote(self):
        source = 'SetColorMode(["#ff0000"])'
        tokens = InputParser.parse(StringIO(source))

        item = tokens[0].args[0].items[0]
        self.assertEqual((1, 15), (item.line, item.column))
        self.assertEqual("#ff0000", item.value)


class EvaluatorErrorUnitTests(unittest.TestCase):
    def test_unknown_function_reports_position(self):
        def Draw():
            pass

        tokens = InputParser.parse(StringIO("Draw()\nSetFoo(1)"))
        evaluator = InputEvaluator([Draw])

        with self.assertRaises(InputError) as context:
            evaluator.parse(tokens)

        error = context.exception
        self.assertEqual(2, error.line)
        self.assertEqual(1, error.column)
        self.assertIn("Unknown function SetFoo", str(error))
        self.assertIn("  SetFoo(1)", str(error))

    def test_value_parser_failure_reports_position(self):
        def Draw(value):
            pass

        def parseTypes(value):
            raise ValueError("not a valid colour")

        tokens = InputParser.parse(StringIO("Draw(notacolour)"))
        evaluator = InputEvaluator([Draw], parseTypes)

        with self.assertRaises(InputError) as context:
            evaluator.parse(tokens)

        error = context.exception
        self.assertEqual(1, error.line)
        self.assertEqual(6, error.column)
        self.assertIn("Could not parse value 'notacolour'", str(error))
        self.assertIn("not a valid colour", str(error))