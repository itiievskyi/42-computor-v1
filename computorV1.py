import argparse
import re
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum, auto, unique

VERBOSE = False
SILENT = False
COLORS = False
REVERSE = False

RESET_COLOR = "\033[0;0m"
REDUCED_COLOR = "\033[30;33m"
DEGREE_COLOR = "\033[30;34m"
ERROR_COLOR = "\033[30;31m"
SOLUTION_COLOR = "\033[30;32m"
STEPS_COLOR = "\033[30;1m"


@dataclass
class SolutionLog:
    steps: List[str]
    degree: str = ""
    reduced: str = ""
    error: str = ""


LOG = SolutionLog(steps=[])


def get_reduced_form(coeffs_all: dict):
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
    reduced = reduced + " = 0" if reduced else "0 = 0"
    return f"Reduced form: {reduced}"


def get_number(line: str):
    if not line:
        return 1
    elif "." in line:
        return float(line)
    else:
        return int(line)


def get_coeffs(raw_code: str) -> Optional[dict]:
    right_side = False
    coeffs = {}

    code = raw_code.lower().replace(" ", "")

    # check for number of vars
    if code.lower().count("x") < 1:
        LOG.error = "Syntax error! No variables detected."
        return

    # check for number of equal signs
    if code.count("=") != 1:
        LOG.error = "Syntax error! Unexpected number of '='."
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
            LOG.error = "Syntax error near '='."
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
            LOG.error = f"Syntax error! Unexpected value: {value!r}"
            return

    # adding zeros explicitly for missing coeffs
    for x in range(3):
        if not coeffs.get(x):
            coeffs[x] = 0

    return dict(sorted({k: v for k, v in coeffs.items()}.items(), reverse=REVERSE))


def get_discriminant(coeffs: dict) -> Optional[int]:
    a, b, c = coeffs.get(2), coeffs.get(1), coeffs.get(0)
    try:
        LOG.steps.append(
            "The equation is complete, calculating discriminant...")
        LOG.steps.append(f"D = `b^2 - 4ac` => `{b}^2 - 4 * {a} * {c}`")
        return b ** 2 - 4 * a * c
    except TypeError:
        LOG.error = "Error during evaluation. Please try again."


def get_incomplete_roots(coeffs: dict) -> List:
    a, b, c = coeffs.get(2), coeffs.get(1), coeffs.get(0)
    LOG.steps.append(
        "The equation is incomplete, discriminant is not required.")
    if a and not b and not c:
        LOG.steps.append("Coefficients: a ≠ 0, b = 0, c = 0.")
        LOG.steps.append(
            "Equation has form `ax^2 = 0`. The one and only solution is `0`."
        )
        return [0]
    elif a and c and not b:
        LOG.steps.append("Coefficients: a ≠ 0, b = 0, c ≠ 0.")
        LOG.steps.append(
            "Equation has form `ax^2 + c = 0`. Checking if `-(c / a)` is positive..."
        )
        if -(c / a) > 0:
            LOG.steps.append(
                f"It's positive. The roots are: `±√(-(c / a))` => `±√(-({c} / {a}))`."
            )
            return [(-c / a) ** (1 / 2), -(-c / a) ** (1 / 2)]
        else:
            LOG.steps.append("It's not positive. There is no valid roots.")
            return []
    elif a and b and not c:
        LOG.steps.append("Coefficients: a ≠ 0, b ≠ 0, c = 0.")
        LOG.steps.append(
            "Equation has form `ax^2 + bx = 0`. It can be transformed into `x(ax + b) = 0`."
        )
        LOG.steps.append(
            f"The roots are `0` and `-(b / a)` => `-({b} / {a})`.")
        return [0, -b / a]
    elif b and c and not a:
        LOG.steps.append("Coefficients: a = 0, b ≠ 0, c ≠ 0.")
        LOG.steps.append("Equation has form `bx + c = 0`, or `bx = c`.")
        LOG.steps.append(
            f"It has only one root: `-(c / b)` => `-({c} / {b})`.")
        return [-c / b]
    elif b and not a and not c:
        LOG.steps.append("Coefficients: a = 0, b ≠ 0, c = 0.")
        LOG.steps.append(
            "Equation has form `bx = 0`. The one and only solution is `0`."
        )
        return [0]
    elif not any([a, b, c]):
        LOG.steps.append("Coefficients: a = 0, b = 0, c = 0.")
        LOG.steps.append(
            "Equation has form `0 = 0`. It means that any real number is the valid root."
        )
        return ["any"]
    return []


def get_roots(discriminant: int, coeffs: dict) -> List:
    a, b, d = coeffs.get(2), coeffs.get(1), discriminant
    if d > 0:  # two solutions
        LOG.steps.append(
            f"Discriminant ({d}) > 0, equation has 2 valid roots.")
        LOG.steps.append(
            f"The roots are: `(-b ±√D) / 2a` => `(-({b}) ±√{d}) / (2 * {a})`"
        )
        return [(-b + d ** (1 / 2)) / (2 * a), (-b - d ** (1 / 2)) / (2 * a)]
    elif d == 0:  # one solution
        LOG.steps.append(f"Discriminant ({d}) = 0, equation has 1 valid root.")
        LOG.steps.append(f"The root is: `-b / 2a` => `-({b}) / (2 * {a})`")
        return [-b / (2 * a)]
    else:  # two solutions with complex numbers
        LOG.steps.append(
            f"Discriminant ({d}) < 0, so equation has no roots among real numbers. But it has two roots among complex numbers."
        )
        LOG.steps.append(
            f"The roots are: `(-b ±i√|D|) / 2a` => `(-({b}) ±(√{abs(d)})i) / (2 * {a})`"
        )
        return [
            complex(-b, abs(d) ** (1 / 2)) / (2 * a),
            complex(-b, -abs(d) ** (1 / 2)) / (2 * a),
        ]


def solve(raw_code: str) -> List[complex or str or float]:
    code = raw_code.lower().replace(" ", "")
    coeffs = get_coeffs(code)
    if not coeffs:
        return

    LOG.reduced = get_reduced_form(coeffs)

    degree = max([k for k, v in coeffs.items() if v] or [0])
    LOG.degree = f"Polynomial degree: {degree}"
    if degree > 2:
        LOG.error = "The polynomial degree is strictly greater than 2, I can't solve."
        return

    roots = []

    if not all([coeffs.get(0), coeffs.get(1), coeffs.get(2)]):
        # specific cases when simpler approach should be used
        roots = get_incomplete_roots(coeffs)
    else:
        # get discriminant
        discriminant = get_discriminant(coeffs)
        if discriminant is None:
            return
        # get roots
        roots = get_roots(discriminant, coeffs)

    return roots


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
        help="Provides detailed information for evaluation steps.",
    )
    parser.add_argument(
        "-s",
        "--silent",
        action="store_true",
        help="Mutes all notifications except solution and errors. Overwrites --verbose flag.",
    )
    parser.add_argument(
        "-r",
        "--reverse",
        action="store_true",
        help="Displays reduced form of equation in standard way: from highest degree to lowest. False by default.",
    )
    parser.add_argument(
        "-c", "--colors", action="store_true", help="Makes output colorful"
    )

    # parsing options and arguments
    args = parser.parse_args()

    # updating global variables based on input
    VERBOSE = args.verbose and not args.silent
    SILENT = args.silent
    COLORS = args.colors
    REVERSE = args.reverse

    # starting evaluation
    roots = solve(args.expression)

    # printing solution with detailed information if needed
    if not SILENT:
        if LOG.reduced:
            print(
                f"{REDUCED_COLOR if COLORS else RESET_COLOR}{LOG.reduced}{RESET_COLOR}"
            )
        if LOG.degree:
            print(
                f"{DEGREE_COLOR if COLORS else RESET_COLOR}{LOG.degree}{RESET_COLOR}")
    if LOG.error:
        print(f"{ERROR_COLOR if COLORS else RESET_COLOR}{LOG.error}{RESET_COLOR}")
    if VERBOSE and LOG.steps:
        print(f"{STEPS_COLOR if COLORS else RESET_COLOR}Steps:{RESET_COLOR}")
        for i in range(len(LOG.steps)):
            print(
                STEPS_COLOR if COLORS else RESET_COLOR,
                f"{i + 1}.",
                LOG.steps[i],
                RESET_COLOR,
            )
    if roots:
        print(
            f"{SOLUTION_COLOR if COLORS else RESET_COLOR}"
            f"The solution is: "
            f"{'any real number' if roots[0] == 'any' else ', '.join([f'{root:.6g}'.replace('j', 'i') for root in roots])}"
            f"{RESET_COLOR}"
        )
    elif not roots and not LOG.error:
        print(
            f"{SOLUTION_COLOR if COLORS else RESET_COLOR}There is no solution{RESET_COLOR}"
        )
