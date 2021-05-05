#!/usr/bin/env python3

import argparse
import sys
import logging
from .query import *
from .summaryB import *
from .summaryN import *
from .taxonB import *
from .compare import comparison, report_bold, report_ncbi


def main():
    """
    Build commandline argument parser and act upon given arguments.
    """
    arguments = argparse.ArgumentParser()
    arguments_sub = arguments.add_subparsers()

    arguments_list = arguments_sub.add_parser('list', help='List databases.')
    arguments_list.set_defaults(action='list')
    arguments_list.add_argument('--bold', action='store_true', help='List BOLD databases.')
    arguments_list.add_argument('--ncbi', action='store_true', help='List NCBI databases.')

    arguments_query = arguments_sub.add_parser('query', help='Search a chosen database for a sequence.')
    arguments_query.set_defaults(action='query')
    arguments_query.add_argument('database', help='Database to be queried.')
    arguments_query.add_argument('sequence', help='File with sequence.')
    arguments_query.add_argument('--out', dest = 'out', help='File for storing results.')

    arguments_summary = arguments_sub.add_parser('summary', help='Display query summary.')
    arguments_summary.set_defaults(action='summary')
    arguments_summary.add_argument('file', help='File with results.')
    arguments_summary.add_argument('--country', action='store_true', help='Display countries of matches.')
    arguments_summary.add_argument('--similarity', action='store_true', help='Display similarities.')
    arguments_summary.add_argument('--score', action='store_true', help='Display scores.')
    arguments_summary.add_argument('--num', dest='num', help='How many records to show.', type=int)
    arguments_summary.add_argument('--identification', action='store_true', help='Display identifiaction.')

    arguments_compare= arguments_sub.add_parser('compare', help='Display found matches.')
    arguments_compare.set_defaults(action='compare')
    arguments_compare.add_argument('file_bold', help='File with BOLD search results.')
    arguments_compare.add_argument('file_ncbi', help='File with NCBI search results.')

    arguments_report = arguments_sub.add_parser('report', help='Report all found matches.')
    arguments_report.set_defaults(action='report')
    arguments_report.add_argument('--bold', dest='bold', help='File with BOLD search results.')
    arguments_report.add_argument('--ncbi', dest='ncbi', help='File with NCBI search results.')

    arguments_taxon = arguments_sub.add_parser('taxon', help='Display taxon information.')
    arguments_taxon.set_defaults(action='taxon')
    arguments_taxon.add_argument('id', help='Identificator - ID or name.')

    if len(sys.argv)<2:
        class HelpConfig:
            def __init__(self):
                self.action = 'help'
        config = HelpConfig()
    else:
        log = logging.getLogger()
        logging.basicConfig(format='%(message)s', level=logging.INFO)
        config = arguments.parse_args()

    if config.action == 'help':
        arguments.print_usage()
        arguments.print_help()
    elif config.action == 'list':
        if config.bold:
            log.info(list_bold())
        elif config.ncbi:
            log.info(list_ncbi())
        else:
            log.info(list_bold() + '\n' + list_ncbi())
    elif config.action == 'query':
        if config.database in ['COX1', 'COX1_SPECIES', 'COX1_SPECIES_PUBLIC', 'COX1_640bp']:
            log.info('Requesting BOLD...')
            query_all(config.database, config.sequence, config.out)
            log.info('Results stored in ' + get_out_file(config.sequence, config.out, config.database))
        else:
            log.info('Requesting NCBI...')
            query_all(config.database, config.sequence, config.out)
            log.info('Results stored in ' + get_out_file(config.sequence, config.out, config.database))
    elif config.action == 'summary':
        if config.file is not None:
            if config.country:
                if config.num is not None:
                    log.info(summary_country(config.file, config.num))
                else:
                    log.info(summary_country(config.file))
            elif config.similarity:
                if config.num is not None:
                    log.info(summary_similarity(config.file, config.num))
                else:
                    log.info(summary_similarity(config.file))
            elif config.score:
                if config.num is not None:
                    log.info(summary_score(config.file, config.num))
                else:
                    log.info(summary_score(config.file))
            elif config.identification:
                if get_database(config.file) in ['COX1', 'COX1_SPECIES', 'COX1_SPECIES_PUBLIC', 'COX1_640bp']:
                    records = summary_identification(config.file)
                    if records:
                        log.info(print_identification(records, config.file))
                    else:
                        log.info('No match found.')
                else:
                    records = NCBI_identification(config.file)
                    if records:
                        log.info(NCBI_print_identification(records, config.file))
                    else:
                        log.info('No match found.')
            else:
                if get_database(config.file) in ['COX1', 'COX1_SPECIES', 'COX1_SPECIES_PUBLIC', 'COX1_640bp']:
                    log.info(summary(config.file))
                else:
                    log.info(NCBI_summary(config.file))
    elif config.action == 'compare':
        log.info(comparison(config.file_bold, config.file_ncbi))
    elif config.action == 'report':
        if config.bold is not None:
            log.info(report_bold(config.bold))
        if config.ncbi is not None:
            log.info(report_ncbi(config.ncbi))
    elif config.action == 'taxon':
        if config.id is not None:
            log.info('Requesting BOLD..')
            log.info(taxon_summary(config.id))
    else:
        arguments.print_usage()
        arguments.print_help()


if __name__ == '__main__':
    main()
