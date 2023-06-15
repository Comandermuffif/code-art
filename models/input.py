import logging
import shlex

from color_modes import ColorMode
from draw_modes import DrawMode

class Token():
        pass

class ValueToken(Token):
    def __init__(self, value:str=None):
        self.value = value

class ArrayToken(Token):
    def __init__(self, items:list[Token] = []):
        self.items = items

class FunctionToken(Token):
    def __init__(self, name:str, args:list[Token] = []):
        self.name = name
        self.args = args

class InputParser():
    @classmethod
    def parse(cls, inputFilepath:str) -> list[tuple[ColorMode, DrawMode]]:
        with open(inputFilepath, mode='r') as stream:
            reader = shlex.shlex(stream)

            while token := reader.get_token():
                logging.debug(token)

                if token == 'SetColorMode':
                    colorMode = cls._parseToken(reader)
                elif token == 'SetDrawMode':
                    drawMode = cls._parseToken(reader)

        raise NotImplementedError()


    @classmethod
    def _parseToken(cls, reader:shlex.shlex) -> Token:
        value = reader.get_token()

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
        name = reader.get_token()
        argsArray = cls._parseArray(reader, '(', ')')
        return FunctionToken(name, argsArray.items)