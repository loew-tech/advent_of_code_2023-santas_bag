import inspect
import re
import sys

from santas_bag.constants import NUMBER_WORDS, WORD_TO_DIGIT
from santas_bag.parse import ints
from santas_bag.utils import get_read_and_solve, get_read_input, get_naughty_or_nice

with open('.env') as f:
    session_ = f.readlines()[0]
read_input = get_read_input(2023, session_)

naughty_or_nice = get_naughty_or_nice(year=2023, session_id=session_)


def day_1(data, part=1, testing=False) -> int:
    if part == 1:
        return day_1_part1(data)
    return day_1_part2(data)

def day_1_part1(data: list[str]) -> int:
    ret = 0
    for d in data:
        print(d)
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


if __name__ == '__main__':
    testing_ = '-t' in sys.argv[1:] or '-testing' in sys.argv[1:]
    print(f'{testing_=}')
    sys_args = [int(i) for i in sys.argv[1:] if i.isnumeric()]
    args_ = sys_args if sys_args else range(1, 26)

    members = inspect.getmembers(inspect.getmodule(inspect.currentframe()))
    funcs = {name: member for name, member in members
             if inspect.isfunction(member)}

    read_and_solve = get_read_and_solve(2023, session_)
    for i in args_:
        day = f'day_{i}'
        if day not in funcs:
            print(f'{day}() = NotImplemented')
            continue


        def part_1(data):
            return funcs[day](data, part=1)


        def part_2(data):
            return funcs[day](data, part=2)

        res1, res2 = read_and_solve(i,
                                    part_1,
                                    part_2,
                                    testing=testing_)
        print(f'* {day}() = {res1}')
        print(f'* {day}(part=2) = {res2}')
