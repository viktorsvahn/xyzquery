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
> xc file.xyz
to count the number of structures contained within the file. (should print all
keys that are possibly shared between all structures and which are not, if there
is a mismatch)

Given two separate files, merge all unique structures with respect to a given
info-key using:
> xc key file1.xyz file2.xyz -m
(NOTE: This allows one to use *.xyz when merging!)


PLAN:
compare keys (are they the same w.r.t a key -> have both pos+force/energies been changed?)
> xc key file1.xyz file2.xyz -c
compare positions (are they the same w.r.t positions -> have force/energies been changed?)
> xc file1.xyz:pos file2.xyz:pos -c
compare forces (are they the same w.r.t forces -> does this contain recomputed forces?)
> xc file1.xyz:forces file2.xyz:forces -c

check for dubplicates in single structure wihtout any flag
> xc key file.xyz
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

merge_help = """
??
"""

sim_help = """
??
"""

compare_help = """
??
"""

output_help = """
output name for merged database
"""


def argument_parser():
    parser = argparse.ArgumentParser(
        prog='xc',
        description=description,
        epilog=epilog,
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        '--version', action='version',
        version=version_help,
    )
    parser.add_argument(
        'handle',
        help=handle_help,
    )
    parser.add_argument(
        'input', nargs='*', default=[],
        help=input_help,
    )
    op = parser.add_argument_group(
        'db operations',
    )
    op.add_argument(
        '-m', '--merge', action='store_true',
        help=merge_help,
    )
    op.add_argument(
        '-c', '--compare', default=False,
        help=compare_help,
    )
    op.add_argument(
        '--check-sim', action='store_true',
        help=sim_help,
    )
    op.add_argument(
        '--keys', action='store_true',
        help=sim_help,
    )
    op.add_argument(
        '-o', '--output', default=False,
        help=output_help,
    )
    
  
    return parser.parse_args()
