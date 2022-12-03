from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    transform = {
        'A': 'R', 'B': 'P', 'C': 'S',
        'X': 'R', 'Y': 'P', 'Z': 'S',
    }
    pick = {'R': 1, 'P': 2, 'S': 3}
    winner = {'R': 'S', 'P': 'R', 'S': 'P'}

    cnt = 0

    for k, v in transform.items():
        s = s.replace(k, v)

    lines = s.splitlines()

    for line in lines:
        one, two = line.split()
        if one == two:
            cnt += 3
        elif winner[one] != two:
            cnt += 6

        cnt += pick[two]

    return cnt


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
