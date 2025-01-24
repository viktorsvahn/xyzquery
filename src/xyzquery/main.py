#!/usr/bin/python

import sys
import numpy as np
import matplotlib.pyplot as plt
from ase.io import read, iread, write

from xyzquery import utils
from xyzquery.parser import argument_parser

args = argument_parser()

class Query:
	def __init__(self, query, atoms):
		# This setup allows for use of '.' in the search query
		qsplit = query.split('.')
		self.property, self.query = qsplit[0], '.'.join(qsplit[1:])

		if self.property == '':
			print('All search queries must have an assigned property.')
			quit()
		elif self.property.lower() == 's':
			self.property = 'symbols'

		if type(atoms) == str:
			self.atoms = iread(atoms, ':')
		else:
			self.atoms = atoms
		
		self.search_string, self.config = self.query_interpreter(self.query, self.property)

		# Makes a trailing ',' equivalent to ':or'
		if '' in self.search_string:
			self.config = ','
			self.search_string.remove('')


	def query_interpreter(self, query, atoms_property):
		# Split query into search_string and config strings
		if ':' in query:
			search_string, config_string = query.split(':')
		else:
			search_string, config_string = query, None

		# Convert element string to element list
		if atoms_property in ('symbols', 's'):
			search_list = utils.string_to_list(search_string, capitalise=True)
		else:
			search_list = utils.string_to_list(search_string, capitalise=False)
		config_list = utils.string_to_list(config_string)

		return search_list, config_list

	def check_search_string(self, structure, search_string):

		if self.property in ('symbols', 's'):
			symbols = str(structure.symbols)
			atoms_property = str(getattr(structure, self.property))
		else:
			try:
				atoms_property = str(structure.info[self.property])
			except:
				print('Invalid property specified. Symbols and info-keys are allowed.')
				quit()

		if 'not' in self.config:
			if all(s not in atoms_property for s in search_string):
				return structure
		else:
			# Must include all search_string
			if ('and' in self.config) and all(s in atoms_property for s in search_string):
				return structure
			# Must include either element
			elif ('or' in self.config) or (',' in self.config):
				if any(s in atoms_property for s in search_string):
					return structure
			# Default behaviour
			elif None in self.config:
				# Given a list, defaults to 'or'
				if len(search_string)>1:
					if any(s in atoms_property for s in search_string):
						return structure
				# Given a single element, defaults to equivalence
				elif search_string[0] == atoms_property:
					return structure

	def find_structures(self):
		query = map(lambda a: self.check_search_string(a, self.search_string), self.atoms)
		new_atoms = filter(lambda a: a is not None, query)
		return new_atoms


def recursive_search(query_list, input_object):
	parsed_query = Query(query_list[0], input_object)
	summary = utils.search_summary(
		config=parsed_query.config[0],
		search_string=parsed_query.search_string,
		atoms_property=parsed_query.property,
	)
	result = list(parsed_query.find_structures())
	if len(query_list) == 1:
		return result
	else:
		return recursive_search(query_list[1:], result)

def plot(title, prop, data):
	index = np.arange(1,len(data)+1)
	plt.xticks(index)
	plt.title(title)
	plt.ylabel(prop)
	plt.xlabel('Structure index')
	plt.plot(index, data, '.-')
	plt.show()

def save(data):
	input_name = args.input.split('.')[0]
	output_name = args.save.split(' ')
	output_name = '-'.join(output_name)
	index = np.arange(1,len(data)+1)
	save_data = np.vstack([index, data]).T
	np.savetxt(
		f'{input_name}_{output_name}.dat',
		save_data,
		header=f'Index {output_name}'
	)


def main():
	# Search
	result = recursive_search(args.query, args.input)
	
	# Saves to file or outputs structure info (text or plot)
	if args.output:
		write(args.output, list(result))
	else:
		data = []
		i=0
		for structure in result:
			i+=1
			
			# Adds number of atoms, energy and force information
			E = structure.get_potential_energy()
			F = structure.get_forces(); Fnorm = np.linalg.norm(F, axis=1)
			structure.info['num_atoms'] = len(structure.numbers)
			structure.info['total_energy'] = E
			structure.info['fmax'] = max(Fnorm)
			
			# drop unwieldy stress array from information
			try:
				del structure.info['stress']
			except:
				pass
			
			# Show output
			print()
			print(f'Structure {i}:')
			utils.print_info(structure)

			# Store plot data in list
			if args.plot:
				data.append(structure.info[args.plot])
			elif args.save:
				data.append(structure.info[args.save])

		print(f'\nNumber of hits: {i}')

		# Plot data
		if args.plot:
			plot(search_summary, args.plot, data)

		if args.save:
			save(data)