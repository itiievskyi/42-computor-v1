from computorV1 import get_coeffs, SolutionLog
import sys

sys.path.append("..")


def test_equal_signs():
    result = get_coeffs("")
    assert not result
