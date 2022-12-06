from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()
    for cnt, line in enumerate(lines):
        # determine max stack height plus identifiers
        if not line:
            id_row = cnt - 1

    stack_positions = []
    for x, stack_num in enumerate(lines[id_row]):
        if stack_num.isdigit():
            stack_count = int(stack_num)
            stack_positions.append(x)

    stacks: list = [[] for _ in range(stack_count)]

    # process the table

    for line in lines:
        if id_row > 0:
            for stack, stack_position in enumerate(stack_positions):
                if line[stack_position] != ' ':
                    stacks[stack].append(line[stack_position])
            id_row -= 1

    for stack in stacks:
        stack.reverse()
        print(stack)

    # process instructions
    for line in lines:
        if line.startswith('move'):
            mve = 3
            frm = 8-1

            while mve > 0:
                stacks[frm].pop()
            mve -= 1
        break

        print(stacks[frm])
    return 0


INPUT_S = '''\

'''
EXPECTED = 1


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
