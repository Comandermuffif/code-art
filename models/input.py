import itertools
import math
import random
import typing
import shlex

class Token():
    pass

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

class InputParser():
    @classmethod
    def parse(cls, stream:typing.TextIO) -> list[Token]:
        reader = shlex.shlex(stream, posix=True)
        tokens = []
        while token := cls._parseToken(reader):
            tokens.append(token)
        return tokens

    @classmethod
    def _parseToken(cls, reader:shlex.shlex) -> Token:
        value = reader.get_token()

        if value == reader.eof:
            return None

        # If we have seen the start of an array
        if value == '[':
            reader.push_token(value)
            return cls._parseArray(reader)

        # Peek at the next token
        nextValue = reader.get_token()
        reader.push_token(nextValue)

        # If it's the start of a function
        if nextValue == '(':
            # Reset the name
            reader.push_token(value)
            return cls._parseFunction(reader)

        return ValueToken(value)

    @classmethod
    def _parseArray(cls, reader:shlex.shlex, start:str='[', end:str=']') -> ArrayToken:
        arrayToken = ArrayToken()

        # Expect the first token to be [
        startChar = reader.get_token()
        if startChar != start:
            raise ValueError(f"Unexpected array start token {startChar}, expected {start}")

        while True:
            token = cls._parseToken(reader)

            if isinstance(token, ValueToken):
                if token.value == end:
                    return arrayToken
                
                if token.value == ',':
                    continue

            arrayToken.items.append(token)

    @classmethod
    def _parseFunction(cls, reader:shlex.shlex) -> FunctionToken:
        funcToken = FunctionToken(reader.get_token())
        argsArray = cls._parseArray(reader, '(', ')')
        funcToken.args = argsArray.items
        return funcToken

class Incrementer():
    index = 0

    @classmethod
    def incremental(cls, values:list[typing.Any]) -> typing.Any:
        return values[cls.index % len(values)]

    @classmethod
    def incrementIndex(cls):
        cls.index += 1

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    return a / b

class InputEvaluator():
    commonFunctuons = [
        add,
        sub,
        mult,
        div,
        sum,
        Incrementer.incremental,
        Incrementer.incrementIndex,
        math.pow,
        math.fsum,
        math.floor,
        math.ceil,
        random.random,
        random.seed,
        random.choice,
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

            raise ValueError(f"Unknown function {token.name}")

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
                parsedValue = self.valueParser(token.value)
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