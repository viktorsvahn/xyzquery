#!/usr/bin/python

import collections
from ase.io import read, iread, write

from xyzcompare.parser import argument_parser

args = argument_parser()

 
class Merge:
	def __init__(self, handle, files):
		self.HANDLE = handle
		self.files = files
		self.NUM_UNIQUE = 0
		
		# Merge
		self.atoms_lists = (iread(f, ':') for f in self.files)
		self.atoms_dict = self.get_unique_structures(self.HANDLE, self.atoms_lists)
		print(f'\nNumber of unique structures: {self.NUM_UNIQUE}')


	def list_to_dict(self, handle, atoms_list):
		atoms_dict = {a.info[handle]:a for a in atoms_list}
		return atoms_dict

	def get_unique_structures(self, handle, atoms_lists):
		merge_string = ' and '.join(self.files)
		if len(self.files) > 1:
			print(f'Merging unique structures in:')
			for m in self.files:
				print(f'  {m}')
			print(f'with respect to \'{handle}\'')
		else:
			print('Single file given.\n')
			print(f'Counting unique structures in:\n  {merge_string}\nwith respect to \'{handle}\'')
		
		
		atoms_dicts = (self.list_to_dict(handle, a) for a in atoms_lists)
		atoms_dict = dict(collections.ChainMap(*atoms_dicts))
		self.NUM_UNIQUE += len(atoms_dict.keys())
		return atoms_dict

	def write_to(self, output):
		atoms_list = list(self.atoms_dict.values())
		print()
		print(f'Saving to: {output}')
		write(output, atoms_list)


def main():


	if args.merge:
		merge = Merge(args.handle, args.input)
		if args.output:
			merge.write_to(args.output)
		elif len(args.input) > 1:
				prompt = input('No output file given. Would you like to save the merged output to a file? (y/[n]): ')
				if prompt.lower() in ('y', 'yes'):
					output = input('Please enter a name for the output file: ')
					print(f'Saving to: {output}')
					merge.write_to(output)
	else:
		print('Please specify an operation')

