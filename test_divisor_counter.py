"""
test_divisor_counter.py

Unit tests for divisor_counter.py following TDD and Clean Code principles.

Run with:
    pytest test_divisor_counter.py -v
"""

import pytest
from divisor_counter import count_divisors, count_valid_n, solve


class TestCountDivisors:

    # --- Positive Tests ---

    def test_one_has_exactly_one_divisor(self):
        assert count_divisors(1) == 1

    def test_prime_two_has_two_divisors(self):
        assert count_divisors(2) == 2

    def test_prime_three_has_two_divisors(self):
        assert count_divisors(3) == 2

    def test_prime_seven_has_two_divisors(self):
        assert count_divisors(7) == 2

    def test_four_is_perfect_square_with_three_divisors(self):
        assert count_divisors(4) == 3

    def test_six_has_four_divisors(self):
        assert count_divisors(6) == 4

    def test_nine_has_three_divisors(self):
        assert count_divisors(9) == 3

    def test_twelve_has_six_divisors(self):
        assert count_divisors(12) == 6

    def test_fourteen_has_four_divisors(self):
        assert count_divisors(14) == 4

    def test_fifteen_has_four_divisors(self):
        assert count_divisors(15) == 4

    def test_sixteen_has_five_divisors(self):
        assert count_divisors(16) == 5

    def test_hundred_has_nine_divisors(self):
        assert count_divisors(100) == 9

    def test_return_type_is_int(self):
        assert isinstance(count_divisors(10), int)

    # --- Negative Tests ---

    def test_zero_raises_value_error(self):
        with pytest.raises(ValueError):
            count_divisors(0)

    def test_negative_number_raises_value_error(self):
        with pytest.raises(ValueError):
            count_divisors(-5)

    def test_large_negative_raises_value_error(self):
        with pytest.raises(ValueError):
            count_divisors(-1000)


class TestCountValidN:

    # --- Positive Tests ---

    def test_k15_returns_two(self):
        assert count_valid_n(15) == 2

    def test_k3_returns_one(self):
        assert count_valid_n(3) == 1

    def test_k4_returns_one(self):
        assert count_valid_n(4) == 1

    def test_k5_returns_one(self):
        assert count_valid_n(5) == 1

    def test_k10_returns_one(self):
        assert count_valid_n(10) == 1

    def test_k2_returns_zero_for_empty_interval(self):
        assert count_valid_n(2) == 0

    def test_k1_returns_zero_for_empty_interval(self):
        assert count_valid_n(1) == 0

    def test_k100_returns_eleven(self):
        assert count_valid_n(100) == 11

    def test_return_type_is_int(self):
        assert isinstance(count_valid_n(15), int)

    def test_result_is_never_negative_across_small_range(self):
        for k in range(1, 20):
            assert count_valid_n(k) >= 0

    def test_count_never_decreases_as_k_grows(self):
        results = [count_valid_n(k) for k in range(2, 50)]
        for i in range(1, len(results)):
            assert results[i] >= results[i - 1]

    # --- Negative Tests ---

    def test_k_zero_raises_value_error(self):
        with pytest.raises(ValueError):
            count_valid_n(0)

    def test_negative_k_raises_value_error(self):
        with pytest.raises(ValueError):
            count_valid_n(-10)

    def test_float_k_raises_type_error(self):
        with pytest.raises(TypeError):
            count_valid_n(15.0)

    def test_string_k_raises_type_error(self):
        with pytest.raises(TypeError):
            count_valid_n("15")

    def test_none_k_raises_type_error(self):
        with pytest.raises(TypeError):
            count_valid_n(None)


class TestSolve:

    # --- Positive Tests ---

    def test_official_example(self):
        assert solve([15]) == [2]

    def test_multiple_cases_returns_correct_length(self):
        assert len(solve([3, 15, 100])) == 3

    def test_k3_in_list(self):
        assert solve([3]) == [1]

    def test_k2_empty_interval(self):
        assert solve([2]) == [0]

    def test_k1_empty_interval(self):
        assert solve([1]) == [0]

    def test_empty_list_returns_empty_list(self):
        assert solve([]) == []

    def test_results_are_non_negative_integers(self):
        for result in solve([1, 2, 3, 5, 10, 15, 50, 100]):
            assert isinstance(result, int)
            assert result >= 0

    def test_return_type_is_list(self):
        assert isinstance(solve([15]), list)

    def test_repeated_k_returns_identical_values(self):
        assert solve([15, 15, 15]) == [2, 2, 2]

    def test_solve_delegates_correctly_to_count_valid_n(self):
        assert solve([100]) == [count_valid_n(100)]

    # --- Negative Tests ---

    def test_integer_argument_raises_type_error(self):
        with pytest.raises(TypeError):
            solve(15)

    def test_tuple_argument_raises_type_error(self):
        with pytest.raises(TypeError):
            solve((15,))

    def test_list_with_negative_k_raises_value_error(self):
        with pytest.raises(ValueError):
            solve([15, -1, 3])

    def test_list_with_float_raises_type_error(self):
        with pytest.raises(TypeError):
            solve([15, 10.5])

    def test_list_with_none_raises_type_error(self):
        with pytest.raises(TypeError):
            solve([15, None])

    def test_list_with_zero_k_raises_value_error(self):
        with pytest.raises(ValueError):
            solve([0])


class TestProblemExampleWalkthrough:

    def test_pair_2_and_3_have_equal_divisors(self):
        assert count_divisors(2) == count_divisors(3)

    def test_pair_14_and_15_have_equal_divisors(self):
        assert count_divisors(14) == count_divisors(15)

    def test_pair_3_and_4_do_not_have_equal_divisors(self):
        assert count_divisors(3) != count_divisors(4)

    def test_full_pipeline_for_official_example(self):
        assert solve([15]) == [2]
