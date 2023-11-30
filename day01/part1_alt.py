from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    print(s)
    lines = s.splitlines()

    elf_sum = 0
    high_sum = 0

    for line in lines:
        if line == '':
            if elf_sum > high_sum:
                high_sum = elf_sum
                print(high_sum)
            elf_sum = 0
            continue

        elf_sum += int(line)
    print()
    return high_sum


INPUT_S = '''
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
'''

EXPECTED = 24000


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
