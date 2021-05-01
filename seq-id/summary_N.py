#!/usr/bin/env python3

from Bio.Blast import NCBIXML
from summary_B import get_seq_name, get_database


def NCBI_summary(file: str) -> str:
    results = open(file)
    blast_record = next(NCBIXML.parse(results))
    res = 'The query results for sequence:' + get_seq_name(file) + \
          """
      Database queried: """ + get_database(file) + \
          """
      Number of hits: """ + get_num_hits(blast_record) + \
          """
      Sequence similarity range: """ + get_range(blast_record) +\
          '\n      ' + print_top_id(get_top_id(file))
    return res


def print_top_id(top: str) -> str:
    result = ''
    for i in top.split(sep='\n'):
        result += i + '\n\t'
    return result[:-4]


def get_num_hits(blast_record) -> str:
    return str(len(blast_record.descriptions))


def get_range(blast_record) -> str:
    return str(blast_record.descriptions[0].score) + ' - ' + str(blast_record.descriptions[-1].score)


def NCBI_identification(file: str) -> str:
    """

    """
    results = open(file)
    blast_record = NCBIXML.read(results)
    records = {}
    for match in blast_record.descriptions:
        score = match.score
        identification = get_name(match.title)
        if identification in records:
            records[identification][1] += 1
            records[identification][0].append(score)
            sorted(records[identification][0])
        else:
            records[identification] = [[score], 1]
    return records


def get_name(record: str) -> str:
    data = record.split(sep=' ')
    return data[1] + ' ' + data[2]


def NCBI_print_identification(records: dict, file: str) -> str:
    """

    """
    sorted_records = {}
    sorted_keys = sorted(records, key=records.get, reverse=True)
    for key in sorted_keys:
        sorted_records[key] = records[key]
    result = 'Taxonomic identification results from NCBI databases for sequence ' + file + ":\n"
    i = 1
    for record in sorted_records:
        result += str(i) + ' ' + record + ' was matched  ' + str(records[record][1]) + \
                  ' times with score ' + get_range_dict(records[record][0]) + '.\n'
        i += 1
    return result


def get_range_dict(records: dict) -> str:
    """

    """
    result = str(records[-1])
    if len(records) > 1:
        result += ' - ' + str(records[0])
    return result


def summary_score(file: str, num: int = 10) -> str:
    """

    """
    results = open(file)
    blast_record = NCBIXML.read(results)
    i = 0
    result = ''
    for align in blast_record.alignments:
        if num <= i:
            break
        i += 1
        a = align.hsps[0]
        result += '_____HIT '+ str(i) + '_____'+\
                  '\n sequence: ' + align.title +\
                  '\n length: ' + str(align.length) +\
                  '\n e value: ' + str(a.expect) +\
                  '\n score: ' + str(a.score) + '\n'
    if i == 0:
        return 'No match found.'
    else:
        return 'Top ' + str(num) + ' matches from NCBI search:\n' + result


def get_top_id(file: str) -> str:
    return 'Top match:\n ' + summary_score(file, 1)[49:]
