import sys

import collections
import re

Token = collections.namedtuple("Token", ["type", "value"])


def tokenize(code):
    pow_0 = 0
    pow_1 = 0
    pow_2 = 0
    right_side = False

    token_specification = [
        (
            "EXPR",
            r"(?P<sign>^|\-|\+|\=){1}((?P<number>\-?[0-9]+(?P<float>\.[0-9]+)?)?((?P<var>\*?x){1}((\^|\*\*)?(?P<power>[0-9]+)))?){1}",
        ),
        ("MISMATCH", r"."),  # Any other character
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        print(mo.groups())
        kind = mo.lastgroup
        value = mo.group()
        if kind == "EXPR":
            sign_multiplicator = (mo.group('sign') == '-') + right_side
            if mo.group('sign') == "=":
                right_side = True
            if not mo.group('var') or (mo.group('power') and int(mo.group('power')) == 0):
                pow_0 = pow_0 + (int(mo.group('number'))
                                 * 1 ** sign_multiplicator)
            elif mo.group('var') and (not mo.group('power') or int(mo.group('power')) == 1):
                pow_1 = pow_1 + (int(mo.group('number'))
                                 * 1 ** sign_multiplicator)
            elif mo.group('var') and mo.group('power') and int(mo.group('power')) == 2:
                pow_2 = pow_2 + (int(mo.group('number'))
                                 * 1 ** sign_multiplicator)
        elif kind == "MISMATCH":
            print(f"Unexpected value: {value!r}")
            return

    print(pow_0, pow_1, pow_2)


if __name__ == "__main__":
    """Entry point"""
    if len(sys.argv) != 2:
        quit("You should provide exactly 1 argument!")

    tokenize(sys.argv[1].lower().replace(" ", ""))
