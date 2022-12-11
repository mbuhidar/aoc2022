from __future__ import annotations

import argparse
import os
from typing import Any

import pytest

import support


INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Knot:

    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    @property
    def pos(self) -> tuple[int, int]:
        return self.x, self.y


class Head(Knot):
    def step(self, direction: str) -> None:
        # move 1 step in the indicated direction
        match direction:
            case 'U':
                self.y += 1
            case 'D':
                self.y -= 1
            case 'L':
                self.x -= 1
            case 'R':
                self.x += 1


class Tail(Knot):
    def __init__(self) -> None:
        super().__init__()
        self.history: set[Any] = set()

    def follow(self, pos: tuple[int, int]) -> None:
        x, y = pos
        dist_x = x - self.x
        dist_y = y - self.y
        if abs(dist_x) == 2 and not dist_y:  # horizontal
            xv = 1 if dist_x > 0 else -1
            self.x += xv
        elif abs(dist_y) == 2 and not dist_x:  # vertical
            yv = 1 if dist_y > 0 else -1
            self.y += yv
        elif (abs(dist_y) == 2 and abs(dist_x) in (1, 2)) or \
             (abs(dist_x) == 2 and abs(dist_y) in (1, 2)):
            xv = 1 if dist_x > 0 else -1
            self.x += xv
            yv = 1 if dist_y > 0 else -1
            self.y += yv
        self.history.add((self.x, self.y))


def compute(s: str) -> int:

    directions = s.splitlines()

    head = Head()
    tails = [Tail() for _ in range(9)]
    for direction in directions:
        dir_, steps = direction.split()
        for _ in range(int(steps)):
            head.step(dir_)
            tails[0].follow(head.pos)
            for i in range(1, 9):
                tails[i].follow(tails[i-1].pos)
    return len(tails[8].history)


INPUT_S = '''\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
'''
EXPECTED = 36


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
