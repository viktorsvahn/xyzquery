#!/usr/bin/python

import collections
import numpy as np
from ase.io import read, iread, write

from xyzcompare.parser import argument_parser

args = argument_parser()

 
class X:
	def __init__(self, handle, files):
		self.HANDLE = handle
		self.files = files
		self.NUM_UNIQUE = 0
		

	def list_to_dict(self, handle, atoms_list):
		atoms_dict = {a.info[handle]:a for a in atoms_list}
		return atoms_dict

	def write_to(self, output):
		atoms_list = list(self.atoms_dict.values())
		print(f'Saving to: {output}')
		write(output, atoms_list)


class MergeFiles(X):
	def __init__(self, *args):
		super().__init__(*args)

		# Merge
		self.atoms_lists = (iread(f, ':') for f in self.files)
		self.atoms_dict = self.get_unique_structures(self.HANDLE, self.atoms_lists)
		print(f'\nNumber of unique structures: {self.NUM_UNIQUE}')


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



class SingleFile(X):
	def __init__(self, *args):
		super().__init__(*args)
		self.FILE = self.HANDLE
		self.atoms = read(self.FILE, ':')
		self.NUM_ATOMS = len(self.atoms)
		
		self.shared_keys, self.non_shared_keys = self.check_shared_keys(self.atoms, key_type= 'info')
		self.shared_arrays, self.non_shared_arrays = self.check_shared_keys(self.atoms, key_type= 'arrays')


	def check_shared_keys(self, atoms, key_type):
		if key_type == 'info':
			all_keys = [set(a.info) for a in atoms]
		elif key_type == 'arrays':
			all_keys = [set(a.calc.results) for a in atoms]
		shared_keys = set.intersection(*all_keys)
		non_shared_keys = set.union(*all_keys) - shared_keys
		return shared_keys, non_shared_keys

	def check_info_similarity(self,atoms1, atoms2):
		print(atoms1.info.values())
		print(atoms2.info.values())
		info_set1 = set(atoms1.info.values())
		info_set2 = set(atoms2.info.values())
		info_check = info_set1 == info_set2
		return info_check

	def measure_similarity(self, bool_list):
		try:
			NUM_ENTRIES = len(bool_list.flatten())
		except:
			NUM_ENTRIES = 1
		NUM_TRUE = np.sum(bool_list)
		NUM_FALSE = NUM_ENTRIES-NUM_TRUE
		SIM_PRCT = int(NUM_TRUE/NUM_ENTRIES*100)
		return SIM_PRCT

	def check_array_similarity(self, dict1, dict2):
		array_check = {
			key1:self.measure_similarity(np.isclose(val1, val2))
			 for (key1,val1), val2 in zip(dict1.items(),dict2.values())
		}
		array_check_bool = map(lambda x: True if x>0 else False, array_check.values())
		return array_check, all(array_check_bool)

	def union_overlapping_sets(self, set_list):
		"""Makes one forward pass of neighbour set reduction by taking the union
		between neighbour sets that overlap.

		Keyword arguments:
		  set_list:  List of k-nary sets of nearest neighbour indices
		"""
		import copy
		tmp = []
		for i, s in enumerate(set_list):
			x = copy.deepcopy(s)
			for j, t in enumerate(set_list):
				if (x != t) and (x&t != set()):
					x = x|t
			if x not in tmp:
				tmp.append(x)
		return tmp


	def check_similarity(self):
		identical = []
		same_info = []
		same_arrays = {}
		same_results = {}
		for i, atoms1 in enumerate(self.atoms):
			for j, atoms2 in enumerate(self.atoms):
				if (i != j) and (i <= self.NUM_ATOMS//2):

					# Symbol and info check
					symbol_check = str(atoms1.symbols) == str(atoms2.symbols)
					if symbol_check:
						print('öjpöjasojopåjdasd')
						info_check = self.check_info_similarity(
							atoms1,
							atoms2
						)

						# Array check: numbers, positions
						array_check, array_check_bool = self.check_array_similarity(
							atoms1.arrays,
							atoms2.arrays,
						)

						# Results check: forces, energies etc
						results_check, results_check_bool = self.check_array_similarity(
							atoms1.calc.results,
							atoms2.calc.results,
						)
						print('FASPLDJASDJSAPIDJASDJP')
						if info_check and array_check_bool and results_check_bool:
							identical.append(set([i+1,j+1]))
						elif info_check:
							same_info.append(set([i+1,j+1]))
						else:
							#if array_check:
							#	same_arrays = {(i+1,j+1):array_check}
							same_arrays[(i+1,j+1)] = array_check
							#if results_check:
							#	same_results = {(i+1,j+1):results_check}
							same_results[(i+1,j+1)] = results_check
		print(same_arrays)
		identical = self.union_overlapping_sets(identical)
		return identical, same_info, same_arrays|same_results


def check_shared_data(shared, non_shared, title):
	print(f'\nThe following {title} are shared between all structures:')
	for key in shared:
		print(f'  {key}')
	if len(non_shared) > 0:
		print(f'\nThe following {title} exist in some of the structures:')
		for key in non_shared:
			print(f'  {key}')
	else:
		print(f'No additional {title} were found.')


def print_similarity(file_object, title):
	if len(file_object) > 0:
		print(title)
		if type(file_object) == list:
			for similarity in file_object:
				print(f'  {similarity}')
		elif type(file_object) == dict:
			for pair, arrays in file_object.items():
				print(f'  Structure {pair[0]} and {pair[1]}:')
				for prop, sim in arrays.items():
					if sim > 0:
						print(f'    {prop} are {sim}% similar')


def main():
	# Single file supplied:
	if '.xyz' in args.handle:
		file_check = SingleFile(args.handle, args.input)

		if args.input == []:
			print(f'The given file contains {file_check.NUM_ATOMS} structures.')

			# identify info-keys and arrays	that are shared between structures
			check_shared_data(
				file_check.shared_keys,
				file_check.non_shared_keys,
				'info-keys',
			)
			check_shared_data(
				file_check.shared_arrays,
				file_check.non_shared_arrays,
				'arrays',
			)

			# Check similarities
			if args.check_sim:
				identical, same_info, same_arrays = file_check.check_similarity()
				print(identical)
				print_similarity(
					identical,
					'\nThe following structures are likely identical:'
				)
				print_similarity(
					same_info,
					'\nThe following structures are likely identical:'
				)
				print_similarity(
					same_arrays,
					'\nThe following additional similarities were found (within a 1e-9 tolerance):'
				)			

	elif args.merge:
		merge = MergeFiles(args.handle, args.input)
		if args.output:
			merge.write_to(args.output)
		elif len(args.input) > 1:
				prompt = input('No output file given. Would you like to save the merged output to a file? (y/[n]): ')
				if prompt.lower() in ('y', 'yes'):
					output = input('Please enter a name for the output file: ')
					merge.write_to(output)
	else:
		print('Please specify an operation')

