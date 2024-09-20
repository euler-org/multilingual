#!/usr/bin/env python
from __future__ import annotations

import json
import shlex
from argparse import ArgumentParser, Namespace
from pathlib import Path
from subprocess import run
from typing import TYPE_CHECKING, Literal, get_args

if TYPE_CHECKING:
    from collections.abc import Iterator

PROJECT_ROOT = Path(__file__).resolve().parents[2]
EULER_ROOT = PROJECT_ROOT.joinpath(".euler")
Languages = Literal["python", "rust"]
LANGUAGES = get_args(Languages)


class InvalidCaseKeys(Exception):
    def __init__(self, invalid_case_keys: set[str]):
        self.invalid_keys = sorted(invalid_case_keys)
        super().__init__(self.error_message)

    @property
    def error_message(self) -> str:
        if len(self.invalid_keys) == 1:
            return f"Case key `{self.invalid_keys[0]}` is not in the statement file."
        joined_keys = (
            f"{', '.join(f'`{key}`' for key in self.invalid_keys[:-1])}"
            " and "
            f"`{self.invalid_keys[-1]}`"
        )
        return f"Case keys {joined_keys} are not in the statement file."


def _get_cases(case_keys: set[str], problem: str) -> Iterator[tuple[str, ...]]:
    statement_file = EULER_ROOT.joinpath("statements", problem).with_suffix(".yaml")
    process = run(
        ["yq"], input=statement_file.read_bytes(), capture_output=True
    )  # noqa: S603
    all_cases = json.loads(process.stdout)["$case_keys"]
    if invalid_case_keys := case_keys.difference(all_cases):
        raise InvalidCaseKeys(invalid_case_keys)
    for case_key in case_keys or all_cases:
        yield case_key, *(str(x) for x in all_cases[case_key])


def get_cases(case_keys: list[str], problem: str) -> list[tuple[str, ...]]:
    return sorted(_get_cases(set(case_keys), problem))


def get_solution(language: Languages, problem: str) -> list[str]:
    match language:
        case "python":
            runner = ["python"]
            executable_dir = PROJECT_ROOT.joinpath(language, "src", "solutions")
            suffix = ".py"
        case "rust":
            runner = []
            executable_dir = PROJECT_ROOT.joinpath(language, "target", "release")
            suffix = ""
    return [*runner, executable_dir.joinpath(problem).with_suffix(suffix).as_posix()]


def parse_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "-l", "--language", type=str, choices=LANGUAGES, default=LANGUAGES[0]
    )
    parser.add_argument("-p", "--problem")
    parser.add_argument("-t", "--times", type=int, default=1)
    parser.add_argument("-c", "--case_keys", nargs="*", default=[])
    return parser.parse_args()


def main() -> None:
    options = parse_args()
    solution = get_solution(options.language, options.problem)
    for case_key, *args in get_cases(options.case_keys, options.problem):
        for _ in range(int(options.times)):
            command = shlex.join([*solution, case_key, *args])
            run(command, shell=True)  # noqa: PLW1510, S603, S607


if __name__ == "__main__":
    main()
