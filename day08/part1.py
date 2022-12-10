from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()

    tree_coords = []

    for row_cnt, line in enumerate(lines):
        max_height = -1
        for col_cnt, tree in enumerate(line):
            height = int(tree)
            if height > max_height:
                max_height = height
                tree_coords.append(tuple((col_cnt, row_cnt)))

    for row_cnt, line in enumerate(lines):
        max_height = -1
        for col_cnt in range(len(line)-1, -1, -1):
            height = int(line[col_cnt])
            if height > max_height:
                max_height = height
                tree_coords.append(tuple((col_cnt, row_cnt)))

    for col_cnt in range(0, len(lines[0])):
        max_height = -1
        for row_cnt, line in enumerate(lines):
            height = int(line[col_cnt])
            if height > max_height:
                max_height = height
                tree_coords.append(tuple((col_cnt, row_cnt)))

    for col_cnt in range(0, len(lines[0])):
        max_height = -1
        for row_cnt in range(len(lines)-1, -1, -1):
            height = int(lines[row_cnt][col_cnt])
            if height > max_height:
                max_height = height
                tree_coords.append(tuple((col_cnt, row_cnt)))

    return len(set(tree_coords))


INPUT_S = '''\
30373
25512
65332
33549
35390
'''
EXPECTED = 21


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
