#!/usr/bin/python


from importlib.metadata import version
import argparse

description = """
CLI for querying extended xyz-format databases.
"""

epilog = """Run:
> xq example.xyz O(,)
to search example.xyz for any structure that contains a single oxygen atom. 
Adding a trailing ',' is intrepreted as an 'or' and will instead result in a 
search for any structure that contains oxygen.

To search for structures that contain either oxygen or nitrogen one may use:
> xq example.xyz O,N
or equivalently:
> xq example.xyz O,N:or

It is possible to include all strucutres that include both by calling:
> xq example.xyz O,N:and
or exclude both using:
> xq example.xyz O,N:not
"""


# 80-23=57 spaces wide

version_help = f'\
xyzquery ver. {version("xyzquery")}'

input_help = """
filename of xyz-database to be queried
"""

query_help = """
element(s) to be searched for in the database.
"""

output_help = """
save queried structures to a new database
"""

plot_help = """
plots a given info-parameter vs structure index
"""

save_help = """
saves a given info-parameter vs structure index to a file
"""



def argument_parser():
    parser = argparse.ArgumentParser(
        prog='xq',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'input',
        help=input_help,
    )
    parser.add_argument(
        'query',
        help=query_help,
    )
    parser.add_argument(
        '-o', '--output', default=False,
        help=output_help,
    )
    parser.add_argument(
        '-p', '--plot', default=False,
        help=plot_help,
    )
    parser.add_argument(
        '-s', '--save', default=False,
        help=save_help,
    )
    """
    parser.add_argument(
        '-m', '--modifier', type=str, 
        help=modifier_help,
    )
    parser.add_argument(
        '-a', '--all', action='store_true',
        help=all_help,
    )
    parser.add_argument(
        '-o', '--output', default=None,
        help=log_help,
    )
    parser.add_argument(
        '-e', '--excluded', nargs='+', default=[],
        help=exclude_help,
    )
    """
    info = parser.add_argument_group(
        'info',
    )
    info.add_argument(
        '--version', action='version',
        version=version_help,
    )
  
    return parser.parse_args()
