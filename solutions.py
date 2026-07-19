import inspect
import re
import sys
from collections import defaultdict
from functools import reduce
from operator import mul
from string import digits
from typing import Tuple

from santas_bag.constants import NUMBER_WORDS, WORD_TO_DIGIT, ALL_DIRECTIONS
from santas_bag.grid import get_inbounds
from santas_bag.parse import ints
from santas_bag.utils import get_read_and_solve, get_read_input, get_naughty_or_nice, read_and_solve

with open('.env') as f:
    session_ = f.readlines()[0]
naughty_or_nice = get_naughty_or_nice(year=2023, session_id=session_)


delims = {
    2: None
}


def day_1(data, part=1) -> int:
    return day_1_part1(data) if part == 1 else day_1_part2(data)


def day_1_part1(data: list[str]) -> int:
    ret = 0
    for d in data:
        first, second = (i:=re.findall(r'\d', d))[0], i[-1]
        ret += int(f'{first}{second}')
    return ret


def day_1_part2(data: list[str]) -> int:
    conversion_dict = {
        **WORD_TO_DIGIT,
        **{str(i): i for i in range(1, 10)}
    }
    pattern = '(?=(' + '|'.join([r'\d', *NUMBER_WORDS]) + '))'
    return sum(int(f'{conversion_dict[re.findall(pattern, line)[0]]}'
                   f'{conversion_dict[re.findall(pattern, line)[-1]]}') for
               line in data)


def parse_day_2(data: str):
    games = defaultdict(lambda: defaultdict(int))
    for ln in data.strip().split('\n'):
        game_str, marbles_ = ln.split(':')
        game = ints(game_str)[0]
        trials = tuple(val.split(' ') for val in marbles_[1:].split('; '))
        for t in trials:
            for i in range(0, len(t), 2):
                val, marble = int(t[i]), t[i + 1].replace(',', '')
                games[game][marble] = max(games[game][marble], val)
    return games


def day_2(data, part=1) -> int:
    print('called day 2')
    return day_2_part1(data) if part == 1 else day_2_part2(data)


def day_2_part1(games: defaultdict) -> int:
    truth = {'red': 12, 'green': 13, 'blue': 14}

    def compare(marbles_: dict) -> bool:
        return not any(truth[k_] < v for k_, v in marbles_.items())
    return sum(k for k, marbles in games.items() if compare(marbles))


def day_2_part2(games: defaultdict) -> int:
    return sum(reduce(mul, marbles.values(), 1) for marbles in games.values())


def day_3(data, part=1) -> int:
    return day_3_part1(data) if part == 1 else day_3_part2(data)


def day_3_part1(grid):
    ignore = {*digits, '.'}
    inbounds = get_inbounds(grid)
    sum_, num, is_part = 0, '', False
    for y, row in enumerate(grid):
        for x, v in enumerate(row):
            if not v.isdigit():
                sum_ += is_part * int(num or '0')
                is_part = False
                num = ''
                continue
            num += v
            for yi, xi in ALL_DIRECTIONS:
                is_part |= inbounds(y + yi, x + xi) and grid[y + yi][x + xi] not in ignore
    return sum_


def day_3_part2(grid) -> int:
    inbounds = get_inbounds(grid)
    def day_3b_helper(y, x: int) -> int:
        def build_digit(y_inc, x_inc: int) -> tuple[set, int]:
            indices = {(y + y_inc, x + x_inc)}
            start_y, start_x = y + y_inc, x + x_inc

            x_left, x_right, val_ = start_x - 1, start_x + 1, grid[start_y][start_x]
            while 0 <= x_left and grid[start_y][x_left] in digits:
                indices.add((start_y, x_left))
                val_ = grid[start_y][x_left] + val_
                x_left -= 1
            while x_right < len(grid[start_y]) and grid[start_y][x_right]\
                    in digits:
                indices.add((start_y, x_right))
                val_ += grid[start_y][x_right]
                x_right += 1

            return indices, int(val_) if val_ else 0

        used_indices, val1, val2 = set(), 0, 0
        for yi, xi in ALL_DIRECTIONS:
            if inbounds(y + yi, x + xi) and grid[y + yi][
                x + xi] in digits \
                    and (y + yi, x + xi) not in used_indices:
                indices_, val = build_digit(yi, xi)
                val1, val2 = (val, val2) if not val1 else (val1, val)
                used_indices.update(indices_)
        return val1 * val2

    return sum(sum((c == '*') * day_3b_helper(y, x) for x, c in
                   enumerate(line)) for y, line in enumerate(grid))


def day_4(data, part=1) -> int:
    return day_4_part1(data) if part == 1 else day_4_part2(data)


def day_4_part1(data: list[str]) -> int:
    score = 0
    for line in data:
        winners, mine = line[line.index(':'):].split('|')
        winners, mine = set(winners.split()), set(mine.split())
        num_matches = len(winners & mine)
        score += 2 ** (num_matches - 1) if num_matches else 0
    return score


def day_4_part2(data: list[str]) -> int:
    card_matches = []
    counts = [1] * len(data)
    for line in data:
        winners, mine = line[line.index(':'):].split('|')
        winners, mine = set(winners.split()), set(mine.split())
        card_matches.append(len(winners & mine))

    for index in range(len(card_matches)):
        for j in range(1, card_matches[index] + 1):
            counts[index + j] += counts[index]
    return sum(counts)



if __name__ == '__main__':
    testing_ = '-t' in sys.argv[1:] or '-testing' in sys.argv[1:]
    sys_args = [int(i) for i in sys.argv[1:] if i.isnumeric()]
    args_ = sys_args if sys_args else range(1, 26)

    members = inspect.getmembers(inspect.getmodule(inspect.currentframe()))
    funcs = {name: member for name, member in members
             if inspect.isfunction(member)}

    parsers = {name: member for name, member in members
             if inspect.isfunction(member) if name.startswith('parse')}

    read_and_solve_ = get_read_and_solve(2023, session_)
    for i in args_:
        day = f'day_{i}'
        if day not in funcs:
            print(f'{day}() = NotImplemented')
            continue

        def part_1(data):
            return funcs[day](data, part=1)


        def part_2(data):
            return funcs[day](data, part=2)

        res1, res2 = read_and_solve_(i,
                                     part_1,
                                     part_2,
                                     delim=delims.get(i, '\n'),
                                     parse=parsers.get(f'parse_day_{i}'),
                                     testing=testing_)
        print(f'* {day}() = {res1}')
        print(f'* {day}(part=2) = {res2}')
