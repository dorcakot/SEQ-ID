#!/usr/bin/env python3

import xml.etree.ElementTree as xml
import requests


def get_taxon_id(sample_id: str) -> str:
    """

    """
    url = 'http://www.boldsystems.org/index.php/API_Public/combined?ids=' + sample_id
    result = requests.get(url)
    return result.text


def get_taxon_name(name: str) -> str:
    """

    """
    url = 'http://www.boldsystems.org/index.php/API_Public/combined?taxon=' + name
    result = requests.get(url)
    return result.text


def taxon_summary(identificator: str) -> str:
    """

    """
    if is_id(identificator):
        data = xml.fromstring(get_taxon_id(identificator))
    else:
        data = xml.fromstring(get_taxon_name(identificator))
    record = data.find('record')
    return 'BOLD record for ' + identificator + ':\n' +\
        get_taxonomy(record) + '\n' +\
        get_collection(record) + '\n' +\
        get_seq(record)


def is_id(identificator: str) -> str:
    """

    """
    if any(char.isdigit() for char in identificator):
        return True
    else:
        return False


def get_taxonomy(record) -> str:
    """

    """
    taxonomy = record.find('taxonomy')
    phylum = taxonomy.find('phylum').find('taxon').find('name').text
    tax_class = taxonomy.find('class').find('taxon').find('name').text
    order = taxonomy.find('order').find('taxon').find('name').text
    family = taxonomy.find('family').find('taxon').find('name').text
    genus = taxonomy.find('genus').find('taxon').find('name').text
    species = taxonomy.find('species').find('taxon').find('name').text
    return 'TAXONOMY:' +\
        '\n Phylum: ' + phylum +\
        '\n Class: ' + tax_class +\
        '\n Order: ' + order +\
        '\n Family: ' + family +\
        '\n Genus: ' + genus +\
        '\n Species: ' + species


def get_collection(record) -> str:
    """

    """
    collection = record.find('collection_event')
    collectors = collection.find('collectors').text
    country = collection.find('country').text
    result=''
    if collectors or country:
        result += 'COLLECTED'
    if collectors:
        result += ' by ' + collectors
    if country:
        result += ' in ' + country
    return result


def get_seq(record) -> str:
    """

    """
    sequences = record.find('sequences')
    sequence = sequences.find('sequence')
    code = sequence.find('markercode').text
    genbank = sequence.find('genbank_accession').text
    seq = sequence.find('nucleotides').text
    res_seq = ''
    for i in range(0, len(seq), 70):
        res_seq += seq[i:i+70] + '\n'
    return 'SEQUENCE ' + code +\
        '\n GenBank Accession: ' + genbank +\
        '\n Nucleotide sequence: ' + str(len(seq)) + 'bp\n' + res_seq