#!/usr/bin/python

import sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from ase.io import read, iread, write

from xyzquery import utils
from xyzquery.parser import argument_parser

args = argument_parser()

class Parse:
	def __init__(self, path, query):
		self.atoms = iread(path, ':')
		self.query = query
		
		self.elements, self.config = self.query_interpreter()

		# Makes a trailing ',' equivalent to ':or'
		if '' in self.elements:
			self.config += ['or']
			self.elements.remove('')


	def query_interpreter(self):
		# Split query into elements and config strings
		if ':' in self.query:
			element_string, config_string = self.query.split(':')
		else:
			element_string, config_string = self.query, None

		# Convert element string to element list
		element_list = utils.string_to_list(element_string)
		config_list = utils.string_to_list(config_string)

		return element_list, config_list

	def check_elements(self, structure, elements):
		symbols = str(structure.symbols)

		if 'not' in self.config:
			if all(e not in symbols for e in elements):
				return structure
		else:
			# Must include all elements
			if ('and' in self.config) and all(e in symbols for e in elements):
				return structure
			# Must include either element
			#elif ('or' in self.config) or ('' in self.elements):
			elif 'or' in self.config:
				if any(e in symbols for e in elements):
					return structure
			# Default behaviour
			elif None in self.config:
				# Given a list, defaults to 'or'
				if len(elements)>1:
					if any(e in symbols for e in elements):
						return structure
				# Given a single element, defaults to equivalence
				elif elements[0] == symbols:
					return structure

	def find_structures(self):
		query = map(lambda a: self.check_elements(a, self.elements), self.atoms)
		new_atoms = filter(lambda a: a is not None, query)
		return new_atoms


def plot(title, prop, index, data):
	index = np.arange(1,len(data)+1)

	plt.xticks(index)
	plt.title(title)
	plt.ylabel(prop)
	plt.xlabel('Structure index')
	plt.plot(index, data, '.-')
	plt.show()


def main():
	# Parse input
	parsed_query = Parse(args.input, args.query) # should generete a list that contains all matches
	
	# Printed search string summary. Should maybe be verbose output
	search_summary = utils.search_summary(parsed_query.config[0], parsed_query.elements)

	# Search
	data = []
	result = parsed_query.find_structures()
	
	# Saves to file or outputs structure info (text or plot)
	if args.output:
		write(args.output, result)
	else:
		i=0
		for structure in result:
			i+=1
			
			# Adds number of atoms, energy and force information
			E = structure.get_potential_energy()
			F = structure.get_forces(); Fnorm = np.linalg.norm(F, axis=1)
			structure.info['num atoms'] = len(structure.numbers)
			structure.info['total energy'] = E
			structure.info['Fmax'] = max(Fnorm)
			
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

			#with open(f'{args.input}_{args.save}.dat', 'w') as f:
			#	f.write(save_data)


if __name__ == '__main__':
	main()