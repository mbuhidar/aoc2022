from __future__ import annotations

import argparse
import os.path
import re
from dataclasses import dataclass
from typing import Any

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Test
# TARGET_ROW = 10
TARGET_ROW = 2000000


@dataclass(frozen=True)
class Point():
    """ Point with x, y coords. Can add a vector, remove a vector,
    and calculate Taxicab distance to to another point. """
    x: int
    y: int

    def __add__(self, other: Point) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point) -> Point:
        return Point(self.x - other.x, self.y - other.y)

    def taxicab_distance_to(self, other: Point) -> int:
        '''Taxicab (aka Manhattan) distance between this vector and another'''
        diff = self - other
        return sum((abs(diff.x), abs(diff.y)))


class SensorGrid():
    """Stores grid of sensors and each sensor's nearest beacon."""

    def __init__(self, sensor_to_beacon: dict[Point, Point]) -> None:
        '''Takes dictionary of sensors and their beacons'''
        self.sensor_to_beacon = sensor_to_beacon
        self.beacons = set(sensor_to_beacon.values())
        self.sensor_range = {
            s: b.taxicab_distance_to(s)
            for s, b in self.sensor_to_beacon.items()
        }

        self._find_boundaries()

    def _find_boundaries(self) -> None:
        ''' Find boundaries by finding min and max values of any scanner
        or beacon and adding to each edge the max distance found for any
        scanner-beacon pair.'''
        max_distance = max(self.sensor_range.items(), key=lambda x: x[1])[1]
        self.min_x = self.max_x = self.min_y = self.max_y = 0
        for s, b in self.sensor_to_beacon.items():
            self.min_x = min([self.min_x, s.x, b.x])
            self.max_x = max([self.max_x, s.x, b.x])
            self.min_y = min([self.min_y, s.y, b.y])
            self.max_y = max([self.max_y, s.y, b.y])

        self.min_x -= max_distance
        self.min_y -= max_distance
        self.max_x += max_distance
        self.max_y += max_distance

    def _get_row_coverage_intervals(self, row: int) -> list[Any]:
        """ For each nearby sensor, get all x intervals for this row.
        Each sensor will return a range of coverage, like [a, b].
        So all sensors will return a list of ranges,
        like [[a, b][c, d][d, e]...]
        """

        # Get only the sensors that are within range of this row
        close_sensors = {
            s: r for s,
            r in self.sensor_range.items() if abs(s.y - row) <= r
        }

        intervals: list[Any] = []  # store start and end y for each sensor

        for sensor, max_rng in close_sensors.items():
            vert_dist_to_row = abs(sensor.y - row)
            max_x_vector = (max_rng - vert_dist_to_row)
            start_x = sensor.x - max_x_vector
            end_x = sensor.x + max_x_vector
            intervals.append([start_x, end_x])

        return intervals

    def _merge_intervals(self, row: int) -> list[Any]:
        '''Takes intervals in the form [[a, b][c, d][d, e]...] and
        intervals can overlap. Compresses to minimum number of non-
        overlapping intervals.'''
        intervals = self._get_row_coverage_intervals(row)
        intervals.sort()
        stack = [intervals[0]]

        for interval in intervals[1:]:
            # Check for overlapping interval
            if stack[-1][0] <= interval[0] <= stack[-1][-1]:
                stack[-1][-1] = max(stack[-1][-1], interval[-1])
            else:
                stack.append(interval)

        return stack

    def coverage_for_row(self, row: int) -> list[Any]:
        return self._merge_intervals(row)

    def __str__(self) -> str:
        rows = []
        for y in range(self.min_y, self.max_y + 1):
            row = ''
            for x in range(self.min_x, self.max_x + 1):
                point = Point(x, y)
                if point in self.sensor_to_beacon.keys():
                    row += 'S'
                elif point in self.beacons:
                    row += 'B'
                else:
                    row += '.'

            rows.append(row)

        return '\n'.join(rows)


def compute(s: str) -> int:

    lines = s.splitlines()
    pattern = re.compile(
        r'[\D]+x=(-?\d+)[\D]+y=(-?\d+)[\D]+x=(-?\d+)[\D]+y=(-?\d+)',
    )
    sensor_to_beacon: dict[Point, Point] = {}
    for line in lines:
        sx, sy, bx, by = map(int, pattern.findall(line)[0])
        sensor_to_beacon[Point(sx, sy)] = Point(bx, by)

    grid = SensorGrid(sensor_to_beacon)

    total_coverage = grid.coverage_for_row(TARGET_ROW)
    coverage_count = sum(
        interval[1]-interval[0] +
        1 for interval in total_coverage
    )
    beacons_to_exclude = sum(
        1 for beacon in grid.beacons if beacon.y == TARGET_ROW
    )

    return coverage_count - beacons_to_exclude


INPUT_S = '''\
Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3
'''
EXPECTED = 26


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
