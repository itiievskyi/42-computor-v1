import sys

import collections
import re

Token = collections.namedtuple('Token', ['type', 'value'])


def tokenize(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        # Integer or decimal number
        ('POW_0',
         r'(?P<sign>^|\-|\+|\=){1}(?P<number>\-?\d+(?P<float>.\d+)?){1}(?P<var>\*?x)?((\^|\*\*){1}(?P<power>\d+)){1}'),
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'POW_0':
            print(f"sign = {mo.group('sign')}")
            print(f"number = {mo.group('number')}")
            print(f"float = {mo.group('float')}")
            print(f"var = {mo.group('var')}")
            print(f"power = {mo.group('power')}")
        elif kind == 'ID' and value in keywords:
            kind = value
        elif kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            print(f"Unexpected value: {value!r}")
            return
        yield Token(kind, value)


if __name__ == "__main__":
    """Entry point"""
    if len(sys.argv) != 2:
        quit("You should provide exactly 1 argument!")

    for token in tokenize(sys.argv[1].lower().replace(' ', '')):
        print(token)
