import typing
import shlex

from color_modes import ColorMode
from draw_modes import DrawMode

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