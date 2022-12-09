from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    # Dictionaries to capture directory names and files
    directories = {'/'}
    files = {}

    pwd = '/'
    lines = s.splitlines()
    for line in lines:
        if line.startswith(('$ ls', 'dir ')):
            # ignore lines without defining info
            continue
        elif line == '$ cd ..':
            # set working directory to next higher level
            pwd = os.path.dirname(pwd)  # or '/'
        elif line.startswith('$ cd'):
            # set working directory to specified path and add to dict
            pwd = os.path.join(pwd, line.split(' ', 2)[-1])
            # print(pwd)
            directories.add(pwd)
        else:
            # capture filename and size in files directory
            size, filename = line.split(' ', 1)
            files[os.path.join(pwd, filename)] = int(size)

    # print(directories)
    # print('\n\n')
    # print(files)

    def get_size(dirname: str) -> int:

        size = 0

        for k, v in files.items():
            if k.startswith(f'{dirname}/'):
                size += v

        return size

    root = sum(files.values())

    size_list = [root] + [get_size(dirname) for dirname in directories]
    size_list.sort()

    delete_need = 30000000 - (70000000 - root)
    size_list = [size for size in size_list if size >= delete_need]
    size_list.sort()

    return size_list[0]


INPUT_S = '''\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
'''
EXPECTED = 24933642


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
