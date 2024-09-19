import sys
from time import perf_counter_ns

from lib.exceptions import UnreachableCodeError
from lib.numbers import is_palindromic


def get_answer(number_of_digits: int) -> int:
    lower_bound: int = 10 ** (number_of_digits - 1)
    upper_bound: int = 10 * lower_bound - 1
    largest_palindrome = 0
    for i in range(upper_bound, lower_bound - 1, -1):
        if i * upper_bound < largest_palindrome:
            return largest_palindrome
        for j in range(upper_bound, i - 1, -1):
            multiple = i * j
            if largest_palindrome > multiple:
                break
            if is_palindromic(multiple):
                largest_palindrome = multiple

    raise UnreachableCodeError


def proxy(case_key: str, number_of_digits: int) -> None:
    begin = perf_counter_ns()
    answer = get_answer(number_of_digits)
    end = perf_counter_ns()
    print(f"Time {case_key} {end - begin}")  # noqa: T201
    print(f"Answer {case_key} {answer}")  # noqa: T201


def main() -> None:
    case_key, number_of_digits = sys.argv[1:]
    proxy(case_key, int(number_of_digits))


if __name__ == "__main__":
    main()
