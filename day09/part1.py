from __future__ import annotations

import argparse
import operator
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input2.txt')


def compute(s: str) -> int:

    lines = s.splitlines()

    head_pos = [0, 0]
    tail_pos = [0, 0]
    tail_cnt = [[0, 0]]

    for line in lines:
        direction = line.split(' ')[0]
        distance = int(line.split(' ')[1])
        if direction == 'R':
            vector = [1, 0]
        elif direction == 'L':
            vector = [-1, 0]
        elif direction == 'D':
            vector = [0, -1]
        elif direction == 'U':
            vector = [0, 1]
        else:
            raise Exception('invalid input')

        for _ in range(distance):
            head_pos = list(map(operator.add, head_pos, vector))
            print(head_pos)

            if tail_pos[0] == head_pos[0]:
                tail_pos = list(map(operator.add, tail_pos, vector))
            elif tail_pos[1] == head_pos[1]:
                tail_pos = list(map(operator.add, tail_pos, vector))
            elif abs(tail_pos[0] - head_pos[0]) > 1:
                pass

            if tail_pos not in tail_cnt:
                tail_cnt.append(tail_pos)

    print(tail_cnt)

    return len(tail_cnt)


'''
        # head_pos = list(map(operator.add, start_pos, vector))
        head_vector = vector

        for _ in range(distance-1):

            if head_vector == [0, 0]:
                pass
            elif head_vector[0] == 0:
                head_vector[1] = int(head_vector[1] / abs(head_vector[1]))
            elif head_vector[1] == 0:
                head_vector[0] = int(head_vector[0] / abs(head_vector[0]))
            else:
                head_vector[0] = int(head_vector[0] / abs(head_vector[0]))
                head_vector[1] = int(head_vector[1] / abs(head_vector[1]))

            head_pos = list(map(operator.add, head_pos, head_vector))

            for _ in range(distance-1):
                tail_vector = list(map(operator.sub, head_pos, tail_pos))

                if tail_vector == [0, 0]:
                    pass
                elif tail_vector[0] == 0:
                    tail_vector[1] = int(tail_vector[1] / abs(tail_vector[1]))
                elif tail_vector[1] == 0:
                    tail_vector[0] = int(tail_vector[0] / abs(tail_vector[0]))
                else:
                    tail_vector[0] = int(tail_vector[0] / abs(tail_vector[0]))
                    tail_vector[1] = int(tail_vector[1] / abs(tail_vector[1]))

                tail_pos = list(map(operator.add, tail_pos, tail_vector))

                if tail_pos not in tail_list:
                    tail_list.append(tail_pos)

    positions = len(tail_list)

    print(tail_list, positions)

    return 0
'''

INPUT_S = '''\
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
'''
EXPECTED = 13


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
