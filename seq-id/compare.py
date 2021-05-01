#!/usr/bin/env python3

from summary_B import summary
from summary_N import NCBI_summary


def comparison(bold: str, ncbi: str) -> str:
    """

    """
    b = summary(bold)
    n = NCBI_summary(ncbi)

    result = b.split(sep='\n')[0] + '\n'
    result += ('-'*40) + 'BOLD' + ('-'*20) + 'NCBI' + ('-'*10) +\
        '\n| Database queried: ' + ' '*10 + '| ' + get_data(b, 1) + \
        ' '*(21-len(get_data(b, 1))) + '| ' + get_data(n, 1) + ' '*(22-len(get_data(n, 1))) + '|'
    result += '\n| Number of hits: ' + ' '*12 + '| ' + get_data(b, 2) + \
        ' '*(21-len(get_data(b, 2))) + '| ' + get_data(n, 2) + ' '*(22-len(get_data(n, 2))) + '|'
    result += '\n| Similarity or score range: ' + ' ' + '| ' + get_data(b, 3) + \
              ' ' * (21 - len(get_data(b, 3))) + '| ' + get_data(n, 3) + ' ' * (22 - len(get_data(n, 3))) + '|'
    result += '\n| Top match: ' + ' '*17 + '|  ID ' + get_data(b, 4).split()[3] + \
              ' ' * (17 - len(get_data(b, 4).split()[3])) + '| gi ' + get_data(n, 5).split(sep='|')[1] +\
              ' ' * (19 - len(get_data(n, 5).split(sep='|')[1])) + '|'
    result += '\n|' + ' '*29 + '| ' + get_data(b, 4).split()[6] + ' ' + get_data(b, 4).split()[7] + '| '
    result += get_data(n, 5).split(sep='|')[4].split()[0] + ' ' + get_data(n, 5).split(sep='|')[4].split()[1] + ' |'
    return result


def get_data(data: str, index: int) -> str:
    """

    """
    return data.split(sep='\n')[index].split(sep=':')[1]
