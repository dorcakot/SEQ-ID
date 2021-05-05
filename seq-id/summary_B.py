#!/usr/bin/env python3

import xml.etree.ElementTree as xml


def summary_country(file: str, num: int = 10) -> str:
    """
    Arranges 'num' top matches by the similarity and displays information about collection location.
    :param file: File with BOLD results.
    :param num: Number of sequences to be displayed.
    :return: 'num' matches ordered by similarity with info about collection location.
    """
    data = xml.parse(file)
    root = data.getroot()
    records = []
    for match in root.findall('match'):
        id = match.find('ID').text
        similarity = match.find('similarity').text
        identification = match.find('taxonomicidentification').text
        for specimen in match.findall('specimen'):
            for location in specimen.findall('collectionlocation'):
                country = location.find('country').text
        if country is not None:
            record = (id, country, identification, similarity)
            records.append(record)
    if not records:
        return 'No match found'
    else:
        return print_country(sorted(records, key=lambda x: x[3], reverse=True), file, num)


def print_country(records: list, file: str, num: int = 10) -> str:
    """
    Formats 'num' top matches by the similarity and displays information about collection location.
    :param records: Pre-prepared list of BOLD results.
    :param num: Number of sequences to be displayed.
    :return: 'num' matches ordered by similarity with info about collection location.
    """
    print(num)
    if num >= len(records):
        num = len(records)
    result = 'The top ' + str(num) + ' matches in BOLD database for sequence ' + file + ":\n"
    for i in range(num):
        result += str(i + 1) + ' Sample for sequence with ID ' + records[i][0] + ' from ' + records[i][2] +\
                  ' was collected in  ' + records[i][1] + '.\n'
    return result


def summary_similarity(file: str, num: int = 10) -> str:
    """
    Arranges 'num' top matches by the similarity.
    :param file: File with BOLD results.
    :param num: Number of sequences to be displayed.
    :return: 'num' matches ordered by similarity.
    """
    data = xml.parse(file)
    root = data.getroot()
    records = []
    for match in root.findall('match'):
        id = match.find('ID').text
        similarity = match.find('similarity').text
        identification = match.find('taxonomicidentification').text
        record = (id, similarity, identification)
        records.append(record)
    if not records:
        return 'No match found'
    else:
        return print_similarity(sorted(records, key=lambda x: x[1], reverse=True), file, num)


def print_similarity(records: list, file: str, num: int = 10) -> str:
    """
    Formats information about 'num' top matches ordered by the similarity.
    :param records: Pre-prepared list of records - found matches.
    :param file: File with BOLD results.
    :param num: Number of sequences to be displayed.
    :return: 'num' matches ordered by similarity in readable format.
    """
    if num >= len(records):
        num = len(records)
    result = 'The top ' + str(num) + ' matches in BOLD database for sequence ' + file + ":\n"
    for i in range(num):
        result += str(i + 1) + ' Sequence with ID ' + records[i][0] + ' belonging to ' + records[i][2] + \
                  ' showed similarity ' + records[i][1] + '.\n'
    return result


def summary_identification(file: str) -> str:
    """
    Parse BOLD search results in xml format and return a dictionary informing about species identification
        and how many times was it matched.
    :param file: File containing BOLD search results.
    :return: Dictionary of species identification and their count.
    """
    data = xml.parse(file)
    root = data.getroot()
    records = {}
    for match in root.findall('match'):
        similarity = match.find('similarity').text
        identification = match.find('taxonomicidentification').text
        if identification in records:
            records[identification][1] += 1
            records[identification][0].append(similarity)
            sorted(records[identification][0])
        else:
            records[identification] = [[similarity], 1]
    return records


def print_identification(records: dict, file: str) -> str:
    """
    Formats the summary of all assigned taxonomic identifications and how many samples of each identification was assigned.
    :param records: Pre-prepared dictionary of identifications and their count.
    :param file: file containing the BOLD results.
    :return: Taxonomic identification overview.
    """
    sorted_records = {}
    sorted_keys = sorted(records, key=records.get, reverse=True)
    for key in sorted_keys:
        sorted_records[key] = records[key]
    result = 'Taxonomic identification results from BOLD database for sequence ' + file + ":\n"
    i = 1
    for record in sorted_records:
        result += str(i) + ' ' + record + ' was matched  ' + str(records[record][1]) + \
                  ' times with sequence similarity ' + get_range_dict(records[record][0]) + '.\n'
        i += 1
    return result


def get_range_dict(records: dict) -> str:
    """
    Get range of similarities of all hits in string format - suitable for string concatenation.
    :param records: All records returned by the search in a dictionary.
    :return: Range of score of all hits in string format.
    """
    result = records[-1]
    if len(records) > 1:
        result += ' - ' + records[0]
    return result


def summary(file: str) -> str:
    """
    Function creates a summary of BOLD database search.
    :param file: File containing BOLD data to be summarised.
    :return: Short summary of all the matches returned by BOLD database.
    """
    data = xml.parse(file)
    root = data.getroot()
    res = 'The query results for sequence: ' + get_seq_name(file) +\
        """
    Database queried: """ + get_database(file) +\
        """
    Number of hits: """ + get_num_hits(root) +\
        """
    Sequence similarity range: """ + get_range(root) +\
        """
    Top hit: """ + get_top_id(root)
    return res


def get_seq_name(file: str) -> str:
    """
    Extracts sequence name from a filename.
    :param file: File with BOLD results.
    :return: Sequence name.
    """
    result = ''
    clean = file.split(sep='/')[-1]
    for i in clean.split(sep='_')[:-2]:
        result += i + '_'
    return result[:-1]


def get_database(file: str) -> str:
    """
    Extracts database name from a filename.
    :param file: File with BOLD results.
    :return: Database name.
    """
    data = file.split(sep='_')
    return data[-2]


def get_num_hits(root) -> str:
    """
    Get number of all hits in string format - suitable for string concatenation.
    :param root: Results of a BOLD search - xml data root.
    :return: Number of all hits in string format.
    """
    i = 0
    for match in root.findall('match'):
        i += 1
    return str(i)


def get_range(root) -> str:
    """
    Get range of similarities of all hits in string format - suitable for string concatenation.
    :param root: Results of a BOLD search - xml data root.
    :return: Range of similarities of all hits in string format.
    """
    similarities = []
    for match in root.findall('match'):
        similarity = match.find('similarity').text
        similarities.append(similarity)
    if not similarities:
        return 'No match found'
    else:
        return min(similarities) + ' - ' + max(similarities)


def get_top_id(root) -> str:
    """
    Get information about the top match.
    :param root: Results of a BOLD search - xml data root.
    :return: Return information about the top match.
    """
    top = ('', '', '0')
    for match in root.findall('match'):
        similarity = match.find('similarity').text
        if float(similarity) > float(top[2]):
            top = (match.find('ID').text, match.find('taxonomicidentification').text, similarity)
    if top == ('', '', '0'):
        return 'No match found'
    else:
        return 'Sequence with ID ' + top[0] + ' originating from ' + top[1] + ' with similarity ' + top[2] + '.'
