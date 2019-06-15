import re
import sys


def print_reduced_form(pow_0: int, pow_1: int, pow_2: int):
    # for coeff in coeff
    # reduced
    # if pow_0:

    reduced = f"{pow_0} + {pow_1} * X{f' + {pow_2} * X^2' if pow_2 else ''} = 0"
    print(reduced)


def get_number(line: str):
    if not line:
        return 1
    else:
        return int(line)


def solve(code):
    right_side = False
    coeffs = {}

    token_specification = [
        (
            "EXPR",
            r"(?P<sign>^|\-|\+|\=){1}((?P<number>\-?[0-9]+(?P<float>\.[0-9]+)?)?((?P<var>\*?x){1}((\^|\*\*)?(?P<power>[0-9]+)?))?){1}",
        ),
        ("MISMATCH", r"."),  # Any other character
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == "EXPR":
            if mo.group("sign") == "=":
                right_side = True

            number = get_number(mo.group("number"))
            if number:
                sign_multiplicator = (mo.group("sign") == "-") + right_side
                power = 0
                if mo.group("var"):
                    power = 1 if not mo.group(
                        "power") else int(mo.group("power"))

                if coeffs.get(power):
                    coeffs[power] += (number * pow(-1, sign_multiplicator))
                else:
                    coeffs[power] = (number * pow(-1, sign_multiplicator))

        elif kind == "MISMATCH":
            print(f"Unexpected value: {value!r}")
            return

    coeffs = sorted(coeffs.items())
    print(coeffs)
#    print_reduced_form(pow_0, pow_1, pow_2)


if __name__ == "__main__":
    """Entry point"""
    if len(sys.argv) != 2:
        quit("You should provide exactly 1 argument!")

    solve(sys.argv[1].lower().replace(" ", ""))
