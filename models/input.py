import collections
import io
import itertools
import math
import random
import typing
import shlex

class Token():
    # Where the token appeared in the source text, filled in by InputParser.
    line:typing.Optional[int] = None
    column:typing.Optional[int] = None
    source:typing.Optional[str] = None

class ValueToken(Token):
    def __init__(self, value:str=None):
        self.value = value

    def __repr__(self) -> str:
        return self.value

class ArrayToken(Token):
    def __init__(self):
        self.items:list[Token] = list()

    def __repr__(self) -> str:
        return "[{}]".format(str.join(",", [x.__repr__() for x in self.items]))

class FunctionToken(Token):
    def __init__(self, name:str):
        self.name = name
        self.args:list[Token] = list()

    def __repr__(self) -> str:
        return "{}({})".format(self.name, str.join(",", [x.__repr__() for x in self.args]))

class InputError(ValueError):
    """An error tied to a position in the input source."""

    def __init__(self, detail:str, line:int=None, column:int=None, source:str=None) -> None:
        super().__init__(detail)
        self.detail = detail
        self.line = line
        self.column = column
        self.source = source

    def _location(self) -> str:
        if self.line is None:
            return ""
        if self.column is None:
            return f" at line {self.line}"
        return f" at line {self.line}, column {self.column}"

    def _header(self) -> str:
        return f"{self.detail}{self._location()}"

    def _snippet(self) -> str:
        if not self.source or self.line is None:
            return None

        lines = self.source.split('\n')
        if self.line < 1 or self.line > len(lines):
            return None

        column = self.column if self.column is not None else 1
        return "  {}\n  {}^".format(lines[self.line - 1], " " * max(0, column - 1))

    def __str__(self) -> str:
        header = self._header()
        snippet = self._snippet()
        if snippet is None:
            return header
        return f"{header}\n{snippet}"

class ParseError(InputError):
    def _header(self) -> str:
        if self.line is None:
            return f"Parse error: {self.detail}"
        return f"Parse error{self._location()}: {self.detail}"

class _PositionedShlex(shlex.shlex):
    """Shlex that remembers the source position of every token it hands out."""

    def __init__(self, source:str) -> None:
        super().__init__(io.StringIO(source), posix=True)
        # shlex has its own 'source' attribute (include files), hence the name.
        self._sourceText = source
        self.tokenPosition:typing.Optional[tuple[int, int]] = None
        self._cursor = 0
        self._pushedTokens = collections.deque()
        self._pushedPositions = collections.deque()

    def push_token(self, tok, position:typing.Optional[tuple[int, int]]=None) -> None:
        self._pushedTokens.appendleft(tok)
        self._pushedPositions.appendleft(self.tokenPosition if position is None else position)

    def get_token(self):
        if self._pushedTokens:
            tok = self._pushedTokens.popleft()
            self.tokenPosition = self._pushedPositions.popleft()
            return tok

        tok = super().get_token()
        self.tokenPosition = self._locate(tok)
        return tok

    def _locate(self, text:typing.Optional[str]) -> tuple[int, int]:
        text = text or ""
        index = self._sourceText.find(text, self._cursor)

        if index < 0:
            # The token doesn't appear verbatim (e.g. it contained escapes);
            # fall back to where the previous token ended.
            index = self._cursor
            quote = self._sourceText[index:index + 1]
            if text and quote in ('"', "'"):
                closing = self._sourceText.find(quote, index + 1)
                if closing >= 0:
                    self._cursor = closing + 1
        elif text and index > 0 and self._sourceText[index - 1] in ('"', "'"):
            # Point at the opening quote of a quoted token.
            index -= 1
            self._cursor = index + len(text) + 2
        else:
            self._cursor = index + len(text)

        line = self._sourceText.count('\n', 0, index) + 1
        column = index - self._sourceText.rfind('\n', 0, index)
        return (line, column)

class InputParser():
    @classmethod
    def parse(cls, stream:typing.TextIO) -> list[Token]:
        source = stream.read()
        reader = _PositionedShlex(source)
        tokens = []

        try:
            while token := cls._parseToken(reader):
                if isinstance(token, ValueToken) and token.value in (')', ']'):
                    raise cls._error(reader, f"unexpected {token.value!r} - nothing is open to close",
                                     (token.line, token.column))
                tokens.append(token)
        except InputError:
            raise
        except ValueError as ex:
            # shlex failures such as an unterminated quotation
            raise ParseError(str(ex), reader.lineno, None, source) from ex

        return tokens

    @classmethod
    def _parseToken(cls, reader:shlex.shlex) -> Token:
        value, valuePosition = cls._get(reader)

        if value == reader.eof:
            return None

        # A '(' where a value was expected; functions must name themselves first
        if value == '(':
            raise cls._error(reader, "unexpected '(' - expected a value, array, or function name", valuePosition)

        # If we have seen the start of an array
        if value == '[':
            cls._push(reader, value, valuePosition)
            return cls._parseArray(reader)

        # Peek at the next token
        nextValue, nextPosition = cls._get(reader)
        cls._push(reader, nextValue, nextPosition)

        # If it's the start of a function
        if nextValue == '(':
            # Reset the name
            cls._push(reader, value, valuePosition)
            return cls._parseFunction(reader)

        return cls._locateToken(ValueToken(value), reader, valuePosition)

    @classmethod
    def _parseArray(cls, reader:shlex.shlex, start:str='[', end:str=']', description:str=None) -> ArrayToken:
        if description is None:
            description = "array" if start == '[' else "argument list"

        arrayToken = ArrayToken()

        # Expect the first token to be the opening character
        openToken, openPosition = cls._get(reader)
        if openToken != start:
            raise cls._error(reader, f"expected {start!r} to open {description}, found {openToken!r}", openPosition)
        cls._locateToken(arrayToken, reader, openPosition)

        while True:
            token = cls._parseToken(reader)

            if token is None:
                raise cls._error(reader, f"unterminated {description} - expected {end!r} before end of file",
                                 openPosition)

            if isinstance(token, ValueToken):
                if token.value == end:
                    return arrayToken

                if token.value == ',':
                    continue

                if token.value in (')', ']'):
                    openedAt = ""
                    if arrayToken.line is not None:
                        openedAt = f" opened at line {arrayToken.line}, column {arrayToken.column}"
                    raise cls._error(reader,
                                     f"unexpected {token.value!r} - expected {end!r} to close {description}{openedAt}",
                                     (token.line, token.column))

            arrayToken.items.append(token)

    @classmethod
    def _parseFunction(cls, reader:shlex.shlex) -> FunctionToken:
        name, namePosition = cls._get(reader)
        funcToken = cls._locateToken(FunctionToken(name), reader, namePosition)
        argsArray = cls._parseArray(reader, '(', ')', f"argument list to {name!r}")
        funcToken.args = argsArray.items
        return funcToken

    @classmethod
    def _get(cls, reader:shlex.shlex) -> tuple:
        value = reader.get_token()
        return value, cls._position(reader)

    @classmethod
    def _push(cls, reader:shlex.shlex, value, position:tuple=None) -> None:
        if isinstance(reader, _PositionedShlex):
            reader.push_token(value, position)
        else:
            reader.push_token(value)

    @classmethod
    def _position(cls, reader:shlex.shlex) -> tuple:
        return getattr(reader, 'tokenPosition', None)

    @classmethod
    def _source(cls, reader:shlex.shlex) -> str:
        return getattr(reader, '_sourceText', None)

    @classmethod
    def _locateToken(cls, token:Token, reader:shlex.shlex, position:tuple=None) -> Token:
        if position is None:
            position = cls._position(reader)
        if position is not None:
            token.line, token.column = position
        token.source = cls._source(reader)
        return token

    @classmethod
    def _error(cls, reader:shlex.shlex, detail:str, position:tuple=None, error:type=ParseError) -> InputError:
        if position is None:
            position = cls._position(reader)
        line, column = position if position else (None, None)
        return error(detail, line, column, cls._source(reader))

class Incrementer():
    index = 0

    @classmethod
    def incremental(cls, values:list[typing.Any]) -> typing.Any:
        return values[cls.index % len(values)]

    @classmethod
    def incrementIndex(cls):
        cls.index += 1

    @classmethod
    def getIncrementIndex(cls):
        return cls.index

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    return a / b

def subset(array, start:int=None, end:int=None):
    if start == None and end==None:
        return array
    elif start == None and end != None:
        return array[:end]
    elif start != None and end == None:
        return array[:end]
    else:
        return array[start:end]

def rotate(array, offset:int):
    offset = offset % len(array)
    if offset == 0:
        return array
    end = offset - len(array)
    return array[offset:] + array[:end]

def reverse(array:list):
    reversed = list(array)
    reversed.reverse()
    return reversed

def shuffle(array:list):
    shuffled = list(array)
    random.shuffle(shuffled)
    return shuffled

class InputEvaluator():
    commonFunctuons = [
        add,
        sub,
        mult,
        div,
        sum,
        Incrementer.incremental,
        Incrementer.incrementIndex,
        Incrementer.getIncrementIndex,
        math.pow,
        math.fsum,
        math.floor,
        math.ceil,
        random.random,
        random.seed,
        random.choice,
        random.randint,
        subset,
        rotate,
        reverse,
        shuffle,
    ]

    def __init__(self, knownFunctions:list[typing.Callable], valueParser:typing.Callable[[str], typing.Any]=None) -> None:
        self.knownFunctions = {
            x.__name__: x
            for x in itertools.chain(self.commonFunctuons, knownFunctions)
        }
        self.valueParser = valueParser

    def parse(self, tokens:list[Token]) -> None:
        for token in tokens:
            self._flatten(token)

    def _flatten(self, token:Token):
        if isinstance(token, FunctionToken):
            if token.name in self.knownFunctions:
                return self.knownFunctions[token.name](*[self._flatten(x) for x in token.args])

            raise InputError(f"Unknown function {token.name}", token.line, token.column, token.source)

        if isinstance(token, ArrayToken):
            return list([self._flatten(x) for x in token.items])

        if isinstance(token, ValueToken):
            if token.value == "$None":
                return None
            elif token.value == "$true":
                return True
            elif token.value == "$false":
                return False

            if self.valueParser:
                try:
                    parsedValue = self.valueParser(token.value)
                except InputError:
                    raise
                except Exception as ex:
                    raise InputError(f"Could not parse value {token.value!r}: {ex}",
                                     token.line, token.column, token.source) from ex
                if parsedValue:
                    return parsedValue

            try:
                return int(token.value)
            except:
                pass

            try:
                return float(token.value)
            except:
                pass

            return token.value

        raise NotImplementedError()