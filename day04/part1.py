from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()

    cnt = 0
    for line in lines:
        elf_set = line.split(',')
        two_elf = []
        for assignment in elf_set:
            elf = assignment.split('-')
            elf_list = []
            for room in range(int(elf[0]), int(elf[1])+1):
                elf_list.append(room)
            two_elf.append(elf_list)

        test1 = set(two_elf[0]).issubset(set(two_elf[1]))
        test2 = set(two_elf[1]).issubset(set(two_elf[0]))

        if test1 or test2:
            cnt += 1

    return cnt


INPUT_S = '''\
34-82,33-81
59-59,69-73
6-96,98-99
1-94,3-96
13-92,20-64
37-75,76-93
5-98,6-6
40-65,40-64
13-63,84-91
31-75,31-35
83-96,86-96
65-85,64-85
2-59,49-58
'''
EXPECTED = 7


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
