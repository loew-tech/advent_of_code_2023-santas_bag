import inspect
import re
import sys
from collections import defaultdict
from functools import reduce
from operator import mul

from santas_bag.constants import NUMBER_WORDS, WORD_TO_DIGIT
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


if __name__ == '__main__':
    testing_ = '-t' in sys.argv[1:] or '-testing' in sys.argv[1:]
    print(f'{testing_=}')
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

        print(f'{i=} {day=} {testing_=} {parsers.get(f"parse_day_{i}")=}')
        input('BREAK: ')
        def part_1(data):
            return funcs[day](data, part=1)


        def part_2(data):
            return funcs[day](data, part=2)

        # @TODO: testing not working (doesn't validate)
        res1, res2 = read_and_solve_(i,
                                     part_1,
                                     part_2,
                                     delim=delims.get(i, '\n'),
                                     parse=parsers.get(f'parse_day_{i}'),
                                     testing=testing_)
        print(f'* {day}() = {res1}')
        print(f'* {day}(part=2) = {res2}')
