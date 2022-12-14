from __future__ import annotations

import argparse
import os.path
import re
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')
RELIEF_FACTOR = 3


def extract_ints(line: str) -> list[int]:
    int_list = [int(i) for i in re.findall(r'(\d+)', line)]
    return int_list


class Monkey:
    def __init__(self, lines: list[str]):
        self.id, = extract_ints(lines[0])
        self.items = extract_ints(lines[1])
        self.operation = lines[2][19:]
        self.test, = extract_ints(lines[3])
        self.true_monkey, = extract_ints(lines[4])
        self.false_monkey, = extract_ints(lines[5])
        self.inspections = 0

    def __repr__(self) -> str:
        return f'Monkey {self.id} ({self.inspections}) {self.items}'

    def apply_operation(self, old: int) -> int:
        return eval(self.operation)

    def throw_to(self, worry_level: int) -> int:
        if worry_level % self.test == 0:
            return self.true_monkey
        else:
            return self.false_monkey

    def take_turn(self, relief_factor: int, monkeys: Any) -> None:
        for worry_level in self.items:
            self.inspections += 1
            worry_level = self.apply_operation(worry_level)
            worry_level //= relief_factor
            target = self.throw_to(worry_level)
            monkeys[target].items.append(worry_level)
        self.items = []


def compute(s: str) -> int:
    inputs = s.split('\n\n')

    monkeys = [Monkey(input.split('\n')) for input in inputs]

    for _ in range(20):
        for monkey in monkeys:
            monkey.take_turn(RELIEF_FACTOR, monkeys)

    inspections = sorted(
        [monkey.inspections for monkey in monkeys], reverse=True,
    )

    return inspections[0] * inspections[1]


INPUT_S = '''\
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
'''
EXPECTED = 10605


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
