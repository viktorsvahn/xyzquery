#!/usr/bin/python


def string_to_list(input_string):
	if (input_string is not None) and (',' in input_string):
		output_list = input_string.split(',')
	else:
		output_list = [input_string]
	return output_list


def search_summary(config, elements):
	if config == 'not':
		summary = 'not '+f' or '.join(elements)
	elif config == 'and':
		summary = f' and '.join(elements)
	elif (config == 'or') or (config == None):
		summary = f' or '.join(elements)

	search_summary = f'Searching for: {summary}'
	print(search_summary)
	return search_summary


def print_info(structure):
	#print()
	longest_key = max([len(s) for s in structure.info]+[16])
	top_spaces = 4+longest_key
	print(f'  Chemical formula{" "*(top_spaces-16)}{structure.symbols}')
	#print(f'  Energy{" "*(top_spaces-6)}{energy}')
	#print(f'  Fmax{" "*(top_spaces-4)}{fmax}')
	
	#print('  Info:')
	for key,val in structure.info.items():
		verbose_spaces = 4+longest_key-len(key)
		print(f'  {key}{" "*verbose_spaces}{val}')