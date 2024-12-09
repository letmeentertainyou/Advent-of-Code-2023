#!/bin/python3.10
"""
I spent like three hours chasing footguns that weren't in the test example. It's very frustrating getting the right answer on the test and now knowing where you went wrong. Overall I spent a lot of
time creating some very sloppy representation for my ranges. Then after I got my answer I cleaned
things up a lot. It feels slow but I'm happy with 3s for a brute force.

real    0m3.462s
user    0m3.448s
sys     0m0.009s
"""

from sys import argv


class Range:
    def __init__(self, start: int, end: int, length: int, value="."):
        self.start = start
        self.end = end
        self.length = length
        self.value = value

    def __str__(self):
        return f"{self.start}, {self.end}, {self.length}, {self.value}"


def mem_map(line: str) -> list:
    """
    00...111...2...333.44.5555.6666.777.888899
    """
    index = 0
    mode = True
    res = []
    for char in line:
        res.extend([index if mode else "." for _ in range(int(char))])
        if mode:
            index += 1
        mode = not mode
    return res


def find_ranges(mapped: list) -> tuple[list]:
    """
    This maps all the ranges of memory to their corresponding characters so that they can be
    processed easier in the final step of the problem.
    """

    def append_range() -> None:
        end = start + length - 1
        if value == ".":
            periods.append(Range(start, end, length))
        else:
            nums.append(Range(start, end, length, value))

    nums, periods = [], []
    value = mapped[0]
    length = 0
    start = 0
    for i, c in enumerate(mapped):
        if c == value:
            length += 1
        else:
            append_range()
            length = 1
            value = c
            start = i

    append_range()
    nums = sorted(nums, key=lambda x: x.value)[::-1]
    return nums, periods


def mem_shift(mapped: list, nums: list[Range], periods: list[Range]) -> list:
    """
    00...111...2...333.44.5555.6666.777.888899
    00992111777.44.333....5555.6666.....8888..
    """

    for r in nums:
        l = r.length
        for _i, c in enumerate(periods):
            # This is the second footgun that the example didn't have.
            if r.start < c.start:
                break

            if l <= c.length:
                for buff in range(l):
                    i1 = r.end - buff
                    i2 = c.start + buff
                    mapped[i1], mapped[i2] = mapped[i2], mapped[i1]
                c.start += l
                c.length -= l
                break
    return mapped


def check_sum(shifted: list) -> int:
    check: int = 0
    for i, c in enumerate(shifted):
        if c != ".":
            check += i * int(c)
    return check


def solve(file: str):
    answer: int = 0
    mapped: list = mem_map(file)
    nums, periods = find_ranges(mapped)
    shifted: list = mem_shift(mapped, nums, periods)
    answer += check_sum(shifted)
    print(answer)


def parse_input(filename: str) -> None:
    with open(filename, "r", encoding="UTF-8") as tmpfile:
        file: str = tmpfile.read()

    solve(file)


if __name__ == "__main__":
    if len(argv) > 1:
        filename = "test.txt"
    else:
        filename = "input.txt"
    print(f"Parsing {filename}.")
    parse_input(filename)


# Test:     2858
# Answer:   6301361958738
# Rank:     7599
