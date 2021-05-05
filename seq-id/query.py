#!/usr/bin/env python3

import glob
import requests
from Bio.Blast import NCBIWWW


def build_url(database: str, sequence: str) -> str:
    """
    URL address builder.
    :param database: database to be queried
    :param sequence: query sequence
    :return: URL address
    """
    with open(sequence, 'r') as f:
        seq = f.readline()
    return 'http://www.boldsystems.org/index.php/Ids_xml?db=' + database + '&sequence=' + seq


def query_bold(database: str, sequence: str) -> str:
    """
    Function queries a database and returns text results.
    :param database: database to be queried
    :param sequence: query sequence
    :return: query text results
    """
    url = build_url(database, sequence)
    result = requests.get(url)
    return result.text


def query_ncbi(database: str, sequence: str) -> str:
    """
    Function queries a database and returns text results.
    :param database: database to be queried
    :param sequence: query sequence
    :return: query text results
    """
    with open(sequence, 'r') as f:
        seq = f.read()
    result_handle = NCBIWWW.qblast("blastn", database, seq, hitlist_size=65)
    return result_handle.read()


def store_query(database: str, sequence: str, file: str) -> None:
    """
    Function stores the results of database query in desired file.
    :param database: database to be queried
    :param sequence: query sequence
    :param file: file where the results will be stored
    """
    with open(file, 'w+') as f:
        if database in ['COX1', 'COX1_SPECIES', 'COX1_SPECIES_PUBLIC', 'COX1_640bp']:
            f.write(query_bold(database, sequence))
        else:
            f.write(query_ncbi(database, sequence))


def query_all(database: str, sequence: str, out: str) -> None:
    """
    Function queries all the files that match given pattern.
    :param database: database to be queried
    :param sequence: query sequence
    :param out: file where the results will be stored
    """
    files = glob.glob(sequence)
    for file in files:
        store_query(database, file, get_out_file(sequence, out, database))


def get_out_file(file: str, specify: str, database: str) -> str:
    """
    A proper name of a file for storing results is created
        - either specified by the user or in format original_name_database_results.
    :param file: Name of a file with a sequence.
    :param specify: User specified file name for storing results.
    :param database: database to be queried
    :return: Name of a file for storing results.
    """
    if specify is not None:
        return specify
    else:
        return file + '_' + database + '_result'


def list_ncbi() -> str:
    """
    :return: Returns list of NCBI databases possible to search.
    """
    return """List of NCBI databases possible to be searched:
    nt: All GenBank + EMBL + DDBJ + PDB sequences. Non-redundant, records with identical sequences collapsed into a single entry.
    rRNA/ITS databases: A collection of four databases: a 16S Microbial rRNA sequences from NCBI’s Targeted Loci \
Projects, an 18S and a 26S RNA rRNA dataabses for fungi, plus an ITS database for fungi.
    refseq_rna: Curated (NM_, NR_) plus predicted (XM_, XR_) sequences from NCBI Reference Sequence Project."""


def list_bold() -> str:
    """
    :return: Returns list of BOLD databases possible to search.
    """
    return """List of BOLD databases possible to be searched:
    COX1 - Every COI barcode record on BOLD with a minimum sequence length of 500bp.
    COX1_SPECIES - Every COI barcode record with a species level identification and a minimum sequence length of 500bp.
    COX1_SPECIES_PUBLIC - All published COI records from BOLD and GenBank with a minimum sequence length of 500bp.
    COX1_L640bp - Subset of the Species library with a minimum sequence length of 640bp and containing both public and \
private records."""
