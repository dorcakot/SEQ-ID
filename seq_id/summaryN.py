#!/usr/bin/env python3

from Bio.Blast import NCBIXML
from .summaryB import get_seq_name, get_database


def NCBI_summary(file: str) -> str:
    """
    Function creates a summary of NCBI search.
    :param file: File containing NCBI data to be summarised.
    :return: Short summary of all the matches returned by NCBI search.
    """
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
    """
    Function extracts only ID and specification of the top hit.
    :param top: Long information about the top hit.
    :return: Shorter information about the top hit.
    """
    result = ''
    for i in top.split(sep='\n'):
        result += i + '\n\t'
    return result[:-4]


def get_num_hits(blast_record) -> str:
    """
    Get number of all hits in string format - suitable for string concatenation.
    :param blast_record: Results of a BLAST search.
    :return: Number of all hits in string format.
    """
    return str(len(blast_record.descriptions))


def get_range(blast_record) -> str:
    """
    Get range of score of all hits in string format - suitable for string concatenation.
    :param blast_record: Results of a BLAST search.
    :return: Range of score of all hits in string format.
    """
    return str(blast_record.descriptions[0].score) + ' - ' + str(blast_record.descriptions[-1].score)


def NCBI_identification(file: str) -> str:
    """
    Parse NCBI search results in xml format and return a dictionary informing about species identification
        and how many times was it matched.
    :param file: File containing NCBI search results.
    :return: Dictionary of species identification and their count.
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
    """
    Extract name of species from long sample data string.
    :param record: Long species database record.
    :return: Name of the species.
    """
    data = record.split(sep=' ')
    return data[1] + ' ' + data[2]


def NCBI_print_identification(records: dict, file: str) -> str:
    """
    Formats a summary of all assigned taxonomic identifications and how many samples of each identification was assigned.
    :param records: Pre-prepared dictionary of identifications and their count.
    :param file: file containing the NCBI results.
    :return: Taxonomic identification overview.
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
    Get range of scores of all hits in string format - suitable for string concatenation.
    :param records: All records returned by the search in a dictionary.
    :return: Range of score of all hits in string format.
    """
    result = str(records[-1])
    if len(records) > 1:
        result += ' - ' + str(records[0])
    return result


def summary_score(file: str, num: int = 10) -> str:
    """
    Arranges 'num' top matches by the score.
    :param file: File with NCBI results.
    :param num: Number of sequences to be displayed.
    :return: 'num' matches ordered by score.
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
    """
    Get information about the top match.
    :param file: File containing search results.
    :return: Return information about the top match.
    """
    return 'Top match:\n ' + summary_score(file, 1)[49:]
