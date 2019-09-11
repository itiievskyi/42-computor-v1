import argparse
import re
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum, auto, unique


@unique
class SolutionType(Enum):
    any_number = auto()
    no_roots = auto()
    real_numbers = auto()
    complex_numbers = auto()


@dataclass
class Solution:
    """Class for storing result in different formats"""

    roots: List[float or complex]
    printable: List[str]

    solution_type: SolutionType = SolutionType.real_numbers


VERBOSE = False
FRACTIONS = False


def print_reduced_form(coeffs_all: dict):
    reduced = ""
    # filtering for correct output
    coeffs = [item for item in coeffs_all.items() if item[1] != 0]
    for coeff in coeffs:
        sign = " + " if coeff[1] > 0 else " - "
        number = abs(coeff[1]) if abs(coeff[1]) > 1 or not coeff[0] else ""
        if coeffs.index(coeff) == 0:
            sign = "-" * bool(coeff[1] < 0)
        var = "X" if coeff[0] else ""
        multiplicator = " * " if abs(coeff[1]) > 1 and var else ""
        power = f"^{coeff[0]}" if coeff[0] > 1 else ""
        reduced += f"{sign}{number}{multiplicator}{var}{power}"
    reduced += " = 0"
    print(reduced)


def get_number(line: str):
    if not line:
        return 1
    elif "." in line:
        return float(line)
    else:
        return int(line)


def get_coeffs(code: str) -> Optional[dict]:
    right_side = False
    coeffs = {}

    # check for number of equal signs
    if code.count("=") != 1:
        print("Unexpected number of '='.")
        return

    token_specification = [
        ("WRONG_EQUALS", r"^=.*|.*=$|=\+|=\*|=\*\*"),
        (
            "EXPR_COEFF",
            r"(?P<sign0>^|\-|\+|\=|\=\-){1}((?P<number0>\-?[0-9]+(?P<float0>\.[0-9]+)?){1}((?P<var0>\*?x){1}((\^|\*\*)?(?P<power0>[0-9]+))?)?){1}",
        ),
        (
            "EXPR_VAR",
            r"(?P<sign1>^|\-|\+|\=|\=\-){1}((?P<number1>\-?[0-9]+(?P<float1>\.[0-9]+)?)?((?P<var1>\*?x){1}((\^|\*\*)?(?P<power1>[0-9]+))?){1}){1}",
        ),
        ("MISMATCH", r"."),  # Any other character
    ]
    tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        valid_tokens = ["EXPR_COEFF", "EXPR_VAR"]
        if kind == "WRONG_EQUALS":
            print("Syntax error near '='.")
            return
        elif kind in valid_tokens:
            if mo.group(f"sign{valid_tokens.index(kind)}") in ["=", "=-"]:
                right_side = True

            number = get_number(mo.group(f"number{valid_tokens.index(kind)}"))
            if number:
                sign_multiplicator = (
                    mo.group(f"sign{valid_tokens.index(kind)}") in ["-", "=-"]
                ) + right_side
                power = 0
                if mo.group(f"var{valid_tokens.index(kind)}"):
                    power = (
                        1
                        if not mo.group(f"power{valid_tokens.index(kind)}")
                        else int(mo.group(f"power{valid_tokens.index(kind)}"))
                    )

                if coeffs.get(power):
                    coeffs[power] += number * pow(-1, sign_multiplicator)
                else:
                    coeffs[power] = number * pow(-1, sign_multiplicator)

        elif kind == "MISMATCH":
            print(f"Unexpected value: {value!r}")
            return

    # adding zeros explicitly for missing coeffs
    for x in range(3):
        if not coeffs.get(x):
            coeffs[x] = 0

    return dict(sorted({k: v for k, v in coeffs.items()}.items()))


def get_discriminant(coeffs: dict) -> int:
    try:
        return coeffs[1] ** 2 - 4 * coeffs[2] * coeffs[0]
    except KeyError:
        quit("Error during evaluation. Please try again.")


def get_printable_roots(
    roots: List[complex or float], solution_type: SolutionType
) -> List[str]:
    if solution_type == SolutionType.real_numbers:
        return [str(root) for root in roots]
    return []


def get_incomplete_roots(coeffs: dict) -> Solution:
    a, b, c = coeffs.get(2), coeffs.get(1), coeffs.get(0)
    if a and not b and not c:
        roots = [0]
        return Solution(
            roots=roots, printable=get_printable_roots(
                roots, SolutionType.real_numbers)
        )
    elif a and c and not b:
        if -(c / a) > 0:
            roots = [(-c / a) ** (1 / 2), -(-c / a) ** (1 / 2)]
            return Solution(
                roots=roots,
                printable=get_printable_roots(
                    roots, SolutionType.real_numbers),
            )
        else:
            return []
    elif a and b and not c:
        return [0, -b / a]
    elif b and c and not a:
        return [-c / b]
    elif b and not a and not c:
        return [0]
    elif not any([a, b, c]):
        return ["any number"]
    return []


def get_roots(discriminant: int, coeffs: dict) -> List:
    a, b, d = coeffs.get(2), coeffs.get(1), discriminant
    if d > 0:  # two solutions
        return [(-b + d ** (1 / 2)) / (2 * a), (-b - d ** (1 / 2)) / (2 * a)]
    elif d == 0:  # one solution
        return [-b / (2 * a)]
    else:  # two solutions with complex numbers
        return [
            complex(-b, abs(d) ** (1 / 2)) / (2 * a),
            complex(-b, -abs(d) ** (1 / 2)) / (2 * a),
        ]


def solve(raw_code: str):
    code = raw_code.lower().replace(" ", "")
    coeffs = get_coeffs(code)
    if not coeffs:
        print("Syntax Error!")
        return

    print_reduced_form(coeffs)

    degree = max(coeffs.keys())
    print(f"Polynomial degree: {degree}")
    if degree > 2:
        print("The polynomial degree is strictly greater than 2, I can't solve.")
        return

    roots = []

    if not all([coeffs.get(0), coeffs.get(1), coeffs.get(2)]):
        # specific cases when simpler approach should be used
        roots = get_incomplete_roots(coeffs)
    else:
        # get discriminant
        discriminant = get_discriminant(coeffs)
        # get roots
        roots = get_roots(discriminant, coeffs)

    print(roots)


if __name__ == "__main__":
    """Entry point"""
    # setting a parser
    parser = argparse.ArgumentParser(
        description="Arguments and options for ComputorV1")
    parser.add_argument(
        "expression", help="expression to be evaluated", type=str)
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="provides detailed information for evaluation steps",
    )

    # parsing options and arguments
    args = parser.parse_args()

    # updating global variables based on input
    VERBOSE = args.verbose

    # starting evaluation
    solve(args.expression)
