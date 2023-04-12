from __future__ import annotations
import re

class Token():
    pass

class FuncToken(Token):
    def __init__(self) -> None:
        self.name:str = None
        self.args:ArrayToken = None

class ValueToken(Token):
    def __init__(self) -> None:
        super().__init__()
        self.value = None

class ArrayToken(Token):
    def __init__(self) -> None:
        super().__init__()
        self.values:list[Token] = []

def parse(input:str) -> Token:
    input = input.replace(' ', '')
    (token, remaining) = _parse(input)
    return token

def _parse(input:str) -> tuple[Token, str]:
    if (input[0] == '['):
        token = ArrayToken()
        (values, remaining) = _parseArray(input[1:], ']')
        token.values = values
        if (remaining[0] == ']'):
            remaining = remaining[1:]
        else:
            raise ValueError()
        return (token, remaining)
    else:
        match = re.match(r'^(\w+)(.*)', input)
        if (match == None):
            return (None, input)
        remaining = match.group(2)
        if (remaining != '' and remaining[0] == '('):
            token = FuncToken()
            token.name = match.group(1)
            (values, remaining) = _parseArray(match.group(2)[1:], ')')
            token.args = values
            return (token, remaining)
        else:
            token = ValueToken()
            token.value = match.group(1)
            return (token, match.group(2))

def _parseArray(input:str, endToken:str) -> tuple[list[ArrayToken], str]:
    values = []
    remaining = input
    while (True):
        (childValue, remaining) = _parse(remaining)
        values.append(childValue)
        if (remaining[0] == ','):
            remaining = remaining[1:]
            continue
        elif (remaining[0] == endToken):
            break
        else:
            raise ValueError(f"Unexpected token {remaining[0]} while parsing array")
    return (values, remaining)



# Voronoi(Gradient([fff100,ff8c00,e81123], 45))
#
# Voronoi(
#   Gradient(
#     [
#       fff100,
#       ff8c00,
#       e81123
#     ],
#     45
#   )
# )
#
