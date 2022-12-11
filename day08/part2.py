from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()
    max_scenic_score = 0

    for col_cnt in range(1, len(lines[0])-1):
        for row_cnt in range(1, len(lines)-1):

            east_cnt = 0
            height = int(lines[row_cnt][col_cnt])
            for i in range(1, len(lines[0])-col_cnt):
                next_height = int(lines[row_cnt][col_cnt+i])
                east_cnt += 1
                if height <= next_height:
                    break

            west_cnt = 0
            height = int(lines[row_cnt][col_cnt])
            for i in range(1, col_cnt+1):
                next_height = int(lines[row_cnt][col_cnt-i])
                west_cnt += 1
                if height <= next_height:
                    break

            south_cnt = 0
            height = int(lines[row_cnt][col_cnt])
            for i in range(1, len(lines)-row_cnt):
                next_height = int(lines[row_cnt+i][col_cnt])
                south_cnt += 1
                if height <= next_height:
                    break

            north_cnt = 0
            height = int(lines[row_cnt][col_cnt])
            for i in range(1, row_cnt+1):
                next_height = int(lines[row_cnt-i][col_cnt])
                north_cnt += 1
                if height <= next_height:
                    break

            scenic_score = east_cnt * west_cnt * south_cnt * north_cnt
            if scenic_score > max_scenic_score:
                max_scenic_score = scenic_score

    return max_scenic_score


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 8


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
