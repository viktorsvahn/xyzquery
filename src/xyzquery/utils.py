#!/usr/bin/python


def string_to_list(input_string, capitalise=False):
	if (input_string is not None) and (',' in input_string):
		output_list = input_string.split(',')
		if capitalise:
			output_list = [s.title() if len(s)<=2 else s for s in output_list]
	else:
		output_list = [input_string]
	return output_list


def search_summary(config, search_string, atoms_property):
	if config == 'not':
		summary = 'not '+f' or '.join(search_string)
	elif config == 'and':
		summary = f' and '.join(search_string)
	elif (config == 'or') or (config == None):
		summary = f' or '.join(search_string)
	elif config == ',':
		if len(search_string) == 1:
			summary = f'presence of {search_string[0]}'
		else:
			summary = f' or '.join(search_string)

	search_summary = f'Searching {atoms_property} for: {summary}'
	print(search_summary)
	return search_summary


def print_info(structure):
	longest_key = max([len(s) for s in structure.info]+[16])
	top_spaces = 4+longest_key

	print(f'  chemical_formula{" "*(top_spaces-16)}{structure.symbols}')
	for key,val in structure.info.items():
		verbose_spaces = 4+longest_key-len(key)
		print(f'  {key}{" "*verbose_spaces}{val}')