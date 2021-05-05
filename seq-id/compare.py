#!/usr/bin/env python3

from summary_B import summary, get_seq_name, summary_similarity
from summary_N import NCBI_summary, summary_score


def comparison(bold: str, ncbi: str) -> str:
    """
    Creates a report comparing both database searches.
    :param bold: File with BOLD search results.
    :param ncbi: File with NCBI search results.
    :return: Nice, readable report comparing both searches.
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
    Extracts desired part of long data string.
    :param data: Data in long format that need to be splitted.
    :param index: Index indicating which part of the data should be returned.
    :return: Desired part of the data.
    """
    return data.split(sep='\n')[index].split(sep=':')[1]


def report_bold(file: str) -> str:
    """
    Function creates a report of BOLD database search suitable for an expert report.
    :param file: File containing BOLD data to be displayed.
    :return: Short overview and a list of all the matches returned by BOLD database.
    """
    result = 'BOLD query results for sequence ' + get_seq_name(file) + ': \n'
    for line in summary(file).split(sep='\n')[1:-1]:
        result += line + '\n'
    result += 'Matched sequences ordered by similarity:\n'
    matches = summary_similarity(file, num=1000).split(sep='\n')[1:]
    for match in matches:
        result += match + '\n'
    return result


def report_ncbi(file: str) -> str:
    """
    Function creates a report of NCBI search suitable for an expert report.
    :param file: File containing NCBI data to be displayed.
    :return: Short overview and a list of all the matches returned by NCBI.
    """
    result = 'NCBI query results for sequence ' + get_seq_name(file) + ': \n'
    for line in NCBI_summary(file).split(sep='\n')[1:-1]:
        result += line + '\n'
    result += 'Matched sequences ordered by score:\n'
    matches = summary_score(file, num=1000).split(sep='\n')[1:]
    for match in matches:
        result += match + '\n'
    return result