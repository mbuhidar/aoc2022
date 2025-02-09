from __future__ import annotations

import math
import time
from dataclasses import dataclass
from pathlib import Path

from PIL import Image

SCRIPT_DIR = Path(__file__).parent
# INPUT_FILE = Path(SCRIPT_DIR, "input.txt")
INPUT_FILE = Path(SCRIPT_DIR, 'input1.txt')

RENDER = True
OUTPUT_FILE = Path(SCRIPT_DIR, 'output.png')


@dataclass(frozen=True)
class Point():
    """ Point class """
    x: int
    y: int


class Grid():
    """ Represents a grid of trees heights """

    def __init__(self, grid_rows: list[list[int]]) -> None:
        """ Expects data in the format...
            [[3, 0, 3, 7, 3], [2, 5, 5, 1, 2], ...] """
        self.rows: list[list[int]] = grid_rows
        print(self.rows)
        self.cols = list(zip(*self.rows))
        print(self.cols)
        self._width = len(self.cols)
        self._height = len(self.rows)
        self.size = self._width * self._height

    def height_at_point(self, point: Point) -> int:
        return self.rows[point.y][point.x]

    def is_visible(self, point: Point) -> bool:
        """ A tree is visible if it is on any edge,
        or if there are no taller trees in the same row or column. """

        # check if it's on an edge
        if point.x == 0 or point.x == self._width-1:
            return True
        if point.y == 0 or point.y == self._height-1:
            return True

        value = self.height_at_point(point)
        # Check if taller than any other tree in the row. If so, it is visible.
        if value > max(self.rows[point.y][0:point.x]):
            return True
        if value > max(self.rows[point.y][point.x+1:]):
            return True

        # Now check the column.
        if value > max(self.cols[point.x][0:point.y]):
            return True
        if value > max(self.cols[point.x][point.y+1:]):
            return True

        return False

    def get_hidden_trees(self) -> set[Point]:
        """ Returns all locations where trees are hidden from view. """
        return {
            Point(x, y) for x in range(self._height)
            for y in range(self._width)
            if not self.is_visible(Point(x, y))
        }

    def get_scenic_scores(self) -> list[int]:
        """ Returns the scenic scores for every tree in the grid """
        scenic_scores = []

        # process across then down
        for y in range(self._width):
            for x in range(self._height):
                point = Point(x, y)
                score = self.get_scenic_score_for_point(point)
                scenic_scores.append(score)

        return scenic_scores

    def get_scenic_score_for_point(self, point: Point) -> int:
        """ Scenic score is given by product of viewing distance in each of
        the four directions.  Viewing distance is given by how far away is the
        nearest tree that is at least as tall as this one.
        Viewing distance is always 0 when looking out from an edge. """

        this_value = self.height_at_point(point)

        # Use generators, since we will just keep getting the next tree
        # until we reach a tree at least as tall. In theory, this is slightly
        # more efficient than lists.
        left = (x for x in reversed(self.rows[point.y][0:point.x]))
        right = (x for x in self.rows[point.y][point.x+1:])
        up = (y for y in reversed(self.cols[point.x][0:point.y]))
        down = (y for y in self.cols[point.x][point.y+1:])

        viewing_distances = []  # store our four distances
        for direction in (left, right, up, down):
            # if we're on the edge, this will be the final score.
            distance = 0
            for value in direction:
                if value < this_value:
                    distance += 1
                else:  # this tree is at least as tall as our tree.
                    # We can't see past it.
                    distance += 1  # This is the last tree we can see
                    break  # exit inner for

            viewing_distances.append(distance)

        return math.prod(viewing_distances)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}'
            + f'(size={self.size},rows={len(self.rows)},cols={len(self.cols)})'
        )

    def render_image(self, target_width: int = 600) -> Image.Image:
        """ Render grid as a heatmap image
        Args:
            width (int, optional): Target width, in pxiels. Defaults to 600.
        """
        scale = target_width // self._width
        # our original image is only a few pixels across. We need to scale up.

        hidden_trees = self.get_hidden_trees()

        # Flatten our x,y array into a single list of height values
        # If the tree is a hidden tree,
        # set its height to -1 in the flattened array
        height_values = [
            self.height_at_point(Point(x, y))
            if Point(x, y) not in hidden_trees else -1
            for y in range(self._height)
            for x in range(self._width)
        ]

        max_height = max(height_values)

        # create a new list of RGB values,
        # where each is given by an (R,G,B) tuple.
        # To achieve a yellow->amber->red effect, we want R to always be 255,
        # B to always be 0, and G to vary based on height
        pixel_colour_map = list(
            map(
                lambda x: (
                    255, int(255*((max_height-x)/max_height)),
                    0,
                ) if x >= 0 else (0, 0, 0),
                height_values,
            ),
        )

        image = Image.new(mode='RGB', size=(self._width, self._height))
        image.putdata(pixel_colour_map)  # load our colour map into the image

        # scale the image and return it
        return image.resize(
            (self._width*scale, self._height*scale),
            Image.Resampling.NEAREST,
        )


def main() -> None:
    with open(INPUT_FILE, mode='rt') as f:
        data = f.read().splitlines()

    rows = [[int(x) for x in row] for row in data]
    grid = Grid(rows)
    print(grid)

    # Part 1 - How many visible trees?
    hidden_trees = grid.get_hidden_trees()
    print('Part 1:')
    print(f'Number of hidden trees={len(hidden_trees)}')
    print(f'Number of visible trees={grid.size - len(hidden_trees)}')

    # Part 2 - What is the maximum scenic score?
    print('\nPart 2:')
    scenic_scores = grid.get_scenic_scores()
    print(f'Highest score={max(scenic_scores)}')

    if RENDER:
        dir_path = Path(OUTPUT_FILE).parent
        if not Path.exists(dir_path):
            Path.mkdir(dir_path)

        image = grid.render_image(400)
        image.save(OUTPUT_FILE)


if __name__ == '__main__':
    t1 = time.perf_counter()
    main()
    t2 = time.perf_counter()
    print(f'Execution time: {t2 - t1:0.4f} seconds')
