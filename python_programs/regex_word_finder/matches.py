## Brian Seggebruch -- 873408239 -- search a dictionary using regular expressions

import re
import sys
import string

def lines_matching(file, regexes):
	'''Generator function that yields lines from a file that 
	match given regular expressions'''

	for line in file:
		# yield line if it matches each regex passed to function
		if all(re.search(i, line) for i in regexes):
			yield line
		else:
			pass

def main():

	li_regexes = []
	filenames = []
	argi = 1

	# iterating over our options and handling appropriately
	while argi < len(sys.argv):

		arg = sys.argv[argi]
		
		# if no '-' prefix, then assumed filename
		if arg[0] != '-':
			filenames.append(sys.argv[argi])
			argi += 1

		# specifying the lower bound
		elif arg == '-l':
			lower_bound = int(sys.argv[argi+1])
			li_regexes.append((fr'^.{{{lower_bound},}}$'))
			argi += 1

		# specifying the upper bound
		elif arg == '-u':
			upper_bound = int(sys.argv[argi+1])
			li_regexes.append((fr'^.{{,{upper_bound}}}$'))
			argi += 1

		# specifying which characters to exclude
		elif arg == '-x':
			li_regexes.append((fr'^[^{sys.argv[argi+1]}]*$'))
			argi += 1
		
		# specifying order of characters
		elif arg == '-o':
			string_order = ('*'.join(i for i in sys.argv[argi+1] 
							if i in string.ascii_letters)+'*')
			li_regexes.append((fr'^{string_order}$'))
			argi += 1

		# what words would match from this word if we remove some characters?
		elif arg == '-s':
			string_to_look_in = '?'.join(i for i in sys.argv[argi+1]) + '?'
			li_regexes.append((fr'^{string_to_look_in}$'))
			argi += 1

		else:
			print(f"unrecognized argument: {arg}", file = sys.stderr)

		argi += 1

	# asking for input if no file is passed originally
	if len(filenames) == 0:
		for i in lines_matching(sys.stdin, li_regexes):
			print(i, end = '')

	# calling regex generator for each file passed
	for file in filenames:
		with open(file) as f:
			for i in lines_matching(f, li_regexes):
				print(i, end = '')	

if __name__ == '__main__':
	main()