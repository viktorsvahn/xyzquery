#!/usr/bin/python


from importlib.metadata import version
import argparse

description = """
CLI for merging extended xyz-format databases wihtout duplicates.

The program is based on the atomic simulation environment (ASE) and will use
keys present in the atoms objects info, such as atoms_object.info[handle].

NOTE:
This program will only make sure that the output is unique with respect to the 
given handle, regardless of what the structure/atoms object itself looks like!
"""

epilog = """Run:
> xm handle file1.xyz file2.xyz
in order to merge the files such that the output are structures unique with
respect to the given handle.

If a only a single file is given the program will simply count the number of
unique strucutres with respect to the given handle.
"""


# 80-23=57 spaces wide

version_help = f'\
xyzutils ver. {version("xyzutils")}'

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
        epilog=epilog,
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
    info = parser.add_argument_group(
        'info',
    )
    info.add_argument(
        '--version', action='version',
        version=version_help,
    )
  
    return parser.parse_args()
