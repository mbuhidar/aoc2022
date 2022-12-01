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
    high_sums = []

    for line in lines:
        if line == '':
            if elf_sum > high_sum:
                high_sum = elf_sum
                high_sums.append(high_sum)
                print(high_sum)
                print(high_sums[-3:])
            elf_sum = 0
            continue

        elf_sum += int(line)

    return sum(high_sums[-3:])


INPUT_S = '''\

'''
EXPECTED = 1


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        ('1\r1\r\r2\r4\r\r', 6),
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
