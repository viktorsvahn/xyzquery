#!/usr/bin/python


from importlib.metadata import version
import argparse

description = """
CLI for querying extended xyz-format databases.
"""

epilog = """Run:
> xq example.xyz symbol.O(,)
to search example.xyz for any structure that contains a single oxygen atom. 
Adding a trailing ',' is intrepreted as an 'or' and will instead result in a 
search for any structure that contains oxygen.

To search for structures that contain either oxygen or nitrogen one may use:
> xq example.xyz symbol.O,N
or equivalently:
> xq example.xyz s.O,N:or
where the 's' is a shorthand for symbol.

It is possible to include all strucutres that include both by calling:
> xq example.xyz s.O,N:and
or exclude both using:
> xq example.xyz O,N:not
or to include O and exclude using:
> xq example.xyz s.O, s.N:not

To probe other info-keys, simply exchange 's' with the key in question.
"""


# 80-23=57 spaces wide

version_help = f'\
xyzutils ver. {version("xyzutils")}'

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
plots a given info-key vs structure index
"""

save_help = """
saves a given info-key vs structure index to a file
"""



def argument_parser():
    parser = argparse.ArgumentParser(
        prog='xq',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--version', action='version',
        version=version_help,
    )
    parser.add_argument(
        'input',
        help=input_help,
    )
    parser.add_argument(
        'query', nargs='+', default=[],
        help=query_help,
    )
    op = parser.add_argument_group(
        'db operations',
    )
    op.add_argument(
        '-o', '--output', default=False,
        help=output_help,
    )
    op.add_argument(
        '-p', '--plot', default=False,
        metavar='KEY',
        help=plot_help,
    )
    op.add_argument(
        '-s', '--save', default=False,
        metavar='KEY',
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
    info = parser.add_argument_group(
        'info',
    """
  
    return parser.parse_args()
