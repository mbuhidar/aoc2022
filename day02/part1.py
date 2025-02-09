from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    n = 0

    lines = s.splitlines()

    for line in lines:
        one = ord(line[0]) - 64
        two = ord(line[2]) - 87

        n += two

        if one == two:
            n += 3
        elif line[0] == 'A' and line[2] == 'Y':
            n += 6
        elif line[0] == 'B' and line[2] == 'Z':
            n += 6
        elif line[0] == 'C' and line[2] == 'X':
            n += 6

    return n


INPUT_S = '''\
A X
A Y
A Z
B X
B Y
B Z
C X
C Y
C Z
'''
EXPECTED = 18 + 27


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
