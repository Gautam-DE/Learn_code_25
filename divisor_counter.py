"""
divisor_counter.py

Counts integers n in the open interval (1, k) where
the number of positive divisors of n equals that of n + 1.
"""

import math


MINIMUM_VALID_N = 2
MINIMUM_K = 1


def count_divisors(n: int) -> int:
    if n < 1:
        raise ValueError(f"n must be a positive integer, got {n}")
    return _compute_divisor_count(n)


def _compute_divisor_count(n: int) -> int:
    count = 0
    for i in range(1, math.isqrt(n) + 1):
        if n % i == 0:
            count += 2
            if i * i == n:
                count -= 1
    return count


def count_valid_n(k: int) -> int:
    _validate_k(k)
    return _count_matching_pairs(k)


def _validate_k(k: int) -> None:
    if not isinstance(k, int):
        raise TypeError(f"k must be an integer, got {type(k).__name__}")
    if k < MINIMUM_K:
        raise ValueError(f"k must be a positive integer, got {k}")


def _count_matching_pairs(k: int) -> int:
    return sum(
        1 for n in _candidates(k)
        if _have_equal_divisors(n, n + 1)
    )


def _candidates(k: int):
    return range(MINIMUM_VALID_N, k)


def _have_equal_divisors(a: int, b: int) -> bool:
    return count_divisors(a) == count_divisors(b)


def solve(test_cases: list) -> list:
    if not isinstance(test_cases, list):
        raise TypeError(f"test_cases must be a list, got {type(test_cases).__name__}")
    return [count_valid_n(k) for k in test_cases]


if __name__ == "__main__":
    t = int(input("Enter number of test cases: "))
    cases = [int(input(f"k for test case {i + 1}: ")) for i in range(t)]
    for result in solve(cases):
        print(result)
