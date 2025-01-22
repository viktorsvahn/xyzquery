#!/usr/bin/python


from importlib.metadata import version
import argparse

description = """
CLI for merging extended xyz-format databases wihtout duplicates.
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

handle_help = """
info-handle to be used as structure identifyers
"""

input_help = """
filenames of databases that are supposed to be merged
"""

output_help = """
output name for merged database
"""


def argument_parser():
    parser = argparse.ArgumentParser(
        prog='xm',
        description=description,
        #epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        'handle',
        help=handle_help,
    )
    parser.add_argument(
        'input', nargs='+', default=[],
        help=input_help,
    )
    parser.add_argument(
        '-o', '--output', default=False,
        help=output_help,
    )
    """
    parser.add_argument(
        '-p', '--plot', default=False,
        help=plot_help,
    )
    parser.add_argument(
        '-s', '--save', default=False,
        help=save_help,
    )
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
