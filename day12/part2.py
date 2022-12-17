from __future__ import annotations

import argparse
import os.path
import string
from collections import defaultdict

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()

    points = {}

    graph = defaultdict(list)
    starts, end = [], None

    for y, line in enumerate(lines):
        for x, letter in enumerate(line):
            point = complex(x, y)
            if letter == 'S':
                value = 0
                starts.append(point)
            elif letter == 'a':
                value = 0
                starts.append(point)
            elif letter == 'E':
                value = 25
                end = point
            else:
                value = string.ascii_lowercase.index(letter)

            points[point] = value

    for point in points:
        for neighbor in [1 + 0j, -1 + 0j, 0 + 1j, 0 - 1j]:
            if (point + neighbor) in points:
                graph[point].append(point + neighbor)

    def dijkstra(graph, source):
        Q = list(graph.keys())
        dist = {v: float('inf') for v in graph}
        dist[source] = 0

        while Q:
            u = min(Q, key=dist.get)
            Q.remove(u)

            for v in graph[u]:
                alt = dist[u] + 1
                if alt < dist[v] and points[u] - points[v] <= 1:
                    dist[v] = alt

        return dist

    paths = dijkstra(graph, end)

    return int(min(paths[start] for start in starts))


INPUT_S = '''\
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
'''
EXPECTED = 29


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
