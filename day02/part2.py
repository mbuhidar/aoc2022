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

        if line[2] == 'Z':
            n += 6
            if line[0] == 'A':
                n += 2
            elif line[0] == 'B':
                n += 3
            else:
                n += 1
        elif line[2] == 'X':
            if line[0] == 'A':
                n += 3
            elif line[0] == 'B':
                n += 1
            else:
                n += 2
        else:
            n += 3
            n += one

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
EXPECTED = 27 + 18


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
