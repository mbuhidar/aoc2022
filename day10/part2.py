from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def signal(clock: int, xreg: int, signal_sum: int) -> int:
    if clock in [x for x in range(20, 240, 40)]:
        signal_sum += int(clock * xreg)
        return signal_sum
    else:
        return signal_sum


def compute(s: str) -> str:

    clock = 0
    xreg = 1
    signal_dict = {}
    print_str = ''
    output = ''

    lines = s.splitlines()
    signal_dict.update({clock: [xreg-1, xreg, xreg+1]})
    for line in lines:
        if line == 'noop':
            clock += 1
            signal_dict.update({clock: [xreg-1, xreg, xreg+1]})
        elif line.startswith('addx'):
            clock += 1
            signal_dict.update({clock: [xreg-1, xreg, xreg+1]})
            clock += 1
            xreg += int(line.split()[1])
            signal_dict.update({clock: [xreg-1, xreg, xreg+1]})

    for cycle in range(0, 240):
        if cycle % 40 in signal_dict[cycle]:
            print_str += '#'
        else:
            print_str += '.'

    for cnt, letter in enumerate(print_str):
        line_pos = cnt + 1
        if line_pos in [x for x in range(40, 240, 40)]:
            letter += '\n'
        output += letter

    return output


INPUT_S = '''\
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
'''
EXPECTED = '''\
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
'''.rstrip()


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
