from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    stacks_lines, move_lines = s.split('\n\n')

    stack_positions = []
    stack_count = 0
    stack_lines = stacks_lines.split('\n')[-1]

    for x, stack_num in enumerate(stack_lines):
        if stack_num.isdigit():
            stack_count = int(stack_num)
            stack_positions.append(x)

    stacks: list = [[] for _ in range(stack_count)]

    stacks_lines = stacks_lines.splitlines()[:-1]

    for line in stacks_lines:
        for stack, stack_position in enumerate(stack_positions):
            if stack_position > len(line):
                continue
            if line[stack_position] != ' ':
                stacks[stack].append(line[stack_position])

    for stack in stacks:
        stack.reverse()

# parse movement instructions
    for line in move_lines.splitlines():
        move = int(line.split(' ')[1])
        fr_s = int(line.split(' ')[3]) - 1
        to_s = int(line.split(' ')[5]) - 1

        temp = []
        for _ in range(move):
            temp.append(stacks[fr_s].pop())
        # jemp.reverse()

        for _ in range(move):
            stacks[to_s].append(temp.pop())

    for stack in stacks:
        code = ''.join(stack[-1] if stack else '' for stack in stacks)

    return code


INPUT_S = '''\
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
'''
EXPECTED = 'MCD'


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
