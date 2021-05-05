# SEQ ID

SEQ ID enables the user to search BOLD and NCBI databases. Results of database query will be stored in a file in xml format. Multiple options for displaying results are avaliable.


##### If you want to try SEQ ID and avoid installing Python packages globally (which could break system tools or other projects), create a virtual one following these steps:
```console
$ git clone https://gitlab.mff.cuni.cz/dorcakot/seq-id.git
$ cd seq-id
$ python -m venv venv
$ source venv/bin/activate
$ python setup.py install
```
To finish working the virtual environment just type deactivate in your console.

##### Steps to get SEQ ID running in your local environment without creating a virtual one:
```console
$ git clone https://gitlab.mff.cuni.cz/dorcakot/seq-id.git
$ cd seq-id
$ python setup.py install
``` 
##### SEQ ID USAGE
```console
$ seq_id
positional arguments:
  {list,query,summary,compare,taxon}
    list                List databases.
    query               Search a chosen database for a sequence.
    summary             Display query summary.
    compare             Display found matches.
    taxon               Display taxon information.

optional arguments:
  -h, --help            show this help message and exit
```

##### Searching BOLD
BOLD Systems is a database which offers COI sequences search (via public API). To look for an identification here, run with command `query` and include chosen database, path to sequence file and optionally name of the file to store results.
Path to a file with sequence or wildcard path to multiple sequence files can be inputted. To list possible databases, run `seq-id list --bold`.

*Obtaining results:*
```console
$ seq_id query COX1 unknown_sequence
Requesting BOLD...
Results stored in unknown_sequence_COX1_result
```

Now, file unknown_sequence_COX1_result contains the matches found in BOLD COX1 database in xml format.

*Exploring results:*
First option is to display a simple search summary by specifying the output file:
```console
$ seq_id summary unknown_sequence_COX1_result
The query results for sequence: unknown_sequence
    Database queried: COX1
    Number of hits: 65
    Sequence similarity range: 0.9912 - 0.9978
    Top hit: Sequence with ID GBIR12293-19 originating from Streptopelia decaocto with similarity 0.9978.
```

Next, it is possible to list first n matches ordered by similariy. The default number of displayed matches is 10:
```console
$ seq_id summary unknown_sequence_COX1_result --similarity --num 2
The top 2 matches in BOLD database for sequence unknown_sequence:
1 Sequence with ID GBIR12293-19 belonging to Streptopelia decaocto showed similarity 0.9978.
2 Sequence with ID GBIR10752-19 belonging to Streptopelia decaocto showed similarity 0.9978.
```

Another option is to observe in which countries samples for top n sequences were collected. (considered are only samples with locality information):
```console
$ seq_id summary unknown_sequence_COX1_result --country
The top 10 matches in BOLD database for sequence unknown_sequence:
1 Sample for sequence with ID GBMIN134018-17 belonging to Streptopelia decaocto was collected in  Cyprus.
2 Sample for sequence with ID GBIR5261-13 belonging to Streptopelia decaocto was collected in  Saudi Arabia.
3 Sample for sequence with ID BOTW312-05 belonging to Streptopelia decaocto was collected in  United States.
4 Sample for sequence with ID BOTW082-04 belonging to Streptopelia decaocto was collected in  United States.
5 Sample for sequence with ID BON471-07 belonging to Streptopelia decaocto was collected in  Norway.
6 Sample for sequence with ID BISE187-08 belonging to Streptopelia decaocto was collected in  Sweden.
7 Sample for sequence with ID NLAVE423-11 belonging to Streptopelia decaocto was collected in  Netherlands.
8 Sample for sequence with ID MPBM028-17 belonging to Streptopelia decaocto was collected in  Austria.
9 Sample for sequence with ID GBIR5260-13 belonging to Streptopelia decaocto was collected in  Saudi Arabia.
10 Sample for sequence with ID USNMC138-10 belonging to Streptopelia decaocto was collected in  United Kingdom.
```

Lastly, an overview of assigned taxonomic identification:
```console
$ seq_id summary unknown_sequence_COX1_result --identification
Taxonomic identification results from BOLD database for sequence unknown_sequence:
1 Streptopelia decaocto was matched  62 times with sequence similarity 0.9912 - 0.9978.
2 Streptopelia roseogrisea was matched 3 times with sequence similarity 0.9956 - 0.9956.
```

##### Searching NCBI
NCBI offers a collection of databases which contain nucleotide sequences. To look for an identification here, run with command `query` and include chosen database, path to sequence file and optionally name of the file to store results.
Path to a file with sequence or wildcard path to multiple sequence files can be inputted. To list possible databases, run `seq-id list --ncbi`.

*Obtaining results:*
```console
$ seq_id query nt unknown_sequence
Requesting NCBI...
Results stored in unknown_sequence_nt_result
```

Now, file unknown_sequence_nt_result contains the matches found in GenBank, EMBL, DDBJ and PDB databases in xml format.

*Exploring results:*
First option is to display a simple search summary by specifying the output file:
```console
$ seq_id summary unknown_sequence_nt_result
The query results for sequence: unknown_sequence
      Database queried: nt
      Number of hits: 65
      Sequence similarity range: 458.0 - 407.0
      Top match:
	   sequence: gi|1381394236|ref|NC_037513.1| Streptopelia decaocto mitochondrion, complete genome >gi|1376496320|gb|KY827036.1| Streptopelia decaocto mitochondrion, complete genome
	   length: 17160
	   e value: 0.0
	   score: 458.0
```

Next, it is possible to list first n matches ordered by score. The default number of displayed matches is 10:
```console
$ seq_id summary unknown_sequence_nt_result --score --num 2
Top 2 matches from NCBI search:
_____HIT 1_____
 sequence: gi|1381394236|ref|NC_037513.1| Streptopelia decaocto mitochondrion, complete genome >gi|1376496320|gb|KY827036.1| Streptopelia decaocto mitochondrion, complete genome
 length: 17160
 e value: 0.0
 score: 458.0
_____HIT 2_____
 sequence: gi|1338650941|gb|KY754551.1| Streptopelia decaocto voucher G 565 cytochrome oxidase subunit 1 (COI) gene, partial cds; mitochondrial
 length: 697
 e value: 0.0
 score: 458.0
```

Lastly, an overview of assigned taxonomic identification:
```console
$ seq_id summary unknown_sequence_nt_result --identification
Taxonomic identification results from NCBI databases for sequence unknown_sequence:
1 Streptopelia decaocto was matched  58 times with score 407.0 - 458.0.
2 Streptopelia roseogrisea was matched  7 times with score 434.0 - 455.0.
```

##### Compare results
To compare searches from bothe sources, first run the searches and specify result files.

*Comparing results:*
```console
$ seq_id compare unknown_sequence_COX1_result unknown_sequence_nt_result
The query results for sequence: unknown_sequence
----------------------------------------BOLD--------------------NCBI----------
| Database queried:           |  COX1                |  nt                   |
| Number of hits:             |  65                  |  65                   |
| Similarity or score range:  |  0.9912 - 0.9978     |  458.0 - 407.0        |
| Top match:                  |  ID GBIR12293-19     | gi 1381394236         |
|                             | Streptopelia decaocto| Streptopelia decaocto |
```

##### Explore specimen
Both database searches suggest that the unknown_sequence is from Streptopelia decaocto.
To find out about this or any other specimen, run with `taxon` command and provide an identificator - either BOLD ID or name.
```console
$ seq_id taxon GBIR12293-19
BOLD record for GBIR12293-19:
TAXONOMY:
 Phylum: Chordata
 Class: Aves
 Order: Columbiformes
 Family: Columbidae
 Genus: Streptopelia
 Species: Streptopelia decaocto

SEQUENCE COI-5P
 GenBank Accession: NC_037513
 Nucleotide sequence: 1548bp
GTGACCCTAATCAATCGATGACTATTCTCCACCAACCACAAAGACATCGGCACTCTATACCTGATCTTCG
GTGCATGAGCCGGCATAGTTGGCACCGCACTCAGCCTCCTCATCCGCGCAGAACTAGGACAACCCGGCAC
CCTTCTAGGAGATGACCAAATCTATAATGTAATTGTTACAGCCCATGCCTTCGTAATAATTTTCTTTATA
GTTATACCAATCATAATCGGAGGCTTTGGAAACTGATTAGTTCCCCTTATAATTGGCGCCCCCGACATAG
CATTCCCACGCATAAACAACATAAGCTTCTGACTACTACCCCCATCCTTCCTCCTTCTCCTAGCCTCCTC
TACAATTGAAGCCGGCGCAGGAACAGGGTGAACCGTATATCCTCCCCTAGCTGGTAACCTAGCTCACGCC
GGAGCTTCCGTAGACCTTGCCATCTTCTCCCTCCACCTCGCTGGTATCTCCTCCATCTTAGGGGCCATCA
ACTTTATCACTACCGCCATCAACATAAAACCACCAGCCCTCTCACAATACCAAACCCCACTATTCGTATG
ATCCGTCCTCATCACTGCAGTCCTTCTCCTCCTATCTCTTCCAGTCCTTGCCGCTGGTATCACAATACTA
CTTACAGACCGCAACCTAAACACCACTTTTTTTGACCCTGCTGGCGGAGGTGACCCAGTATTATACCAGC
ACCTATTCTGATTCTTCGGCCACCCTGAAGTTTATATCCTAATTTTACCAGGATTCGGAATCATCTCCCA
TGTGGTAGCCTACTATGCAGGCAAAAAAGAACCCTTCGGCTACATAGGCATAGTATGGGCCATACTATCC
ATTGGATTCCTAGGCTTTATCGTTTGAGCTCACCATATATTTACAGTAGGCATAGACGTAGACACCCGAG
CATACTTCACATCAGCCACTATAATCATTGCCATCCCAACAGGCATCAAAGTCTTCAGCTGACTAGCTAC
CCTCCACGGCGGCACCATCAAATGGGATCCTCCTATACTTTGAGCTCTAGGATTCATCTTCCTTTTCACC
ATCGGAGGTCTAACAGGAATTGTCCTGGCAAACTCCTCCCTAGACATCGCCCTTCACGACACATACTACG
TAGTTGCCCACTTCCACTACGTCCTCTCAATAGGAGCCGTCTTTGCCATTCTAGCAGGATTCACCCACTG
ATTCCCACTACTCACAGGATACACCCTCCACCCCACATGAGCCAAAGCCCACTTCGGGGTCATATTTACC
GGTGTCAACCTAACATTCTTCCCCCAACACTTCCTAGGCCTCGCTGGCATGCCACGACGATATTCAGACT
ACCCAGACGCCTACACCCTATGAAACACTATCTCCTCTATCGGATCATTAATCTCAATAACAGCTGTAAT
CATACTAATATTTATTATCTGAGAAGCTTTCGCATCAAAACGTAAAGTACTACAACCAGAACTCACATCT
ACTAACATTGAATGAATCCACGGCTGCCCACCCCCATACCACACCTTCGAAGAACCAGCTTTCGTCCAAG
TACAAGAA
```

```console
$ seq_id taxon Streptopelia decaocto
BOLD record for Streptopelia decaocto:
TAXONOMY:
 Phylum: Chordata
 Class: Aves
 Order: Columbiformes
 Family: Columbidae
 Genus: Streptopelia
 Species: Streptopelia decaocto
COLLECTED in Sweden
SEQUENCE COI-5P
 GenBank Accession: GU572102
 Nucleotide sequence: 648bp
CTGATCTTCGGTGCATGAGCCGGCATAGTTGGCACCGCACTCAGCCTCCTCATCCGCGCAGAACTAGGAC
AACCCGGCACCCTTCTAGGAGATGACCAAATCTATAATGTAATTGTTACAGCCCATGCCTTCGTAATAAT
TTTCTTTATAGTTATACCAATCATAATCGGAGGCTTTGGAAACTGATTAGTTCCCCTTATAATTGGCGCC
CCCGACATAGCATTCCCACGCATAAACAACATAAGCTTCTGACTACTACCCCCATCCTTCCTCCTTCTCC
TAGCCTCCTCTACAATTGAAGCCGGCGCAGGAACAGGGTGAACCGTATATCCTCCCCTAGCTGGTAACCT
AGCTCACGCCGGAGCTTCCGTAGACCTTGCCATCTTCTCCCTCCACCTCGCTGGTATCTCCTCCATCTTA
GGGGCCATCAACTTTATCACTACCGCCATCAACATAAAACCACCAGCCCTCTCACAATACCAAACCCCAC
TATTCGTATGATCCGTCCTCATCACTGCAGTCCTTCTCCTCCTATCTCTTCCAGTCCTTGCCGCTGGTAT
CACAATACTACTTACAGACCGCAACCTAAACACCACTTTTTTTGACCCTGCTGGCGGAGGTGACCCAGTA
TTATACCAGCACCTATTC
```

##### Create data for expert report
A convenient feature of these tools is the ability to create a report which can be directly used for an expert report.
This report contains a short overview and a list of all the found matches. 
Data from one selected or both databases can be included. This can be done using the `report` command and specifying files
via options `--bold` and `--ncbi`.

```console
$ seq_id report --bold unknown_sequence_COX1_result
BOLD query results for sequence seq: 
    Database queried: COX1
    Number of hits: 65
    Sequence similarity range: 0.9912 - 0.9978
Matched sequences ordered by similarity:
1 Sequence with ID GBIR12293-19 belonging to Streptopelia decaocto showed similarity 0.9978.
2 Sequence with ID GBIR10752-19 belonging to Streptopelia decaocto showed similarity 0.9978.
3 Sequence with ID GBIR10750-19 belonging to Streptopelia decaocto showed similarity 0.9978.
...
63 Sequence with ID GBMIN134843-17 belonging to Streptopelia decaocto showed similarity 0.9934.
64 Sequence with ID GBMIN134869-17 belonging to Streptopelia decaocto showed similarity 0.9912.
65 Sequence with ID GBMIN134844-17 belonging to Streptopelia decaocto showed similarity 0.9912.
```
