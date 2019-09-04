## Brian Seggebruch - 873408239 - program to count frequency of characters

# importing the required sys module
import sys


# creating our main function that counts frequencies
def add_frequencies(d, file, remove_case):
	''' This function counts the number of occurences of letters
	in a file (file) and measures by outputting to dictionary (d). If the
	-c flag is not included, remove_case will be True and each character is added as a key in lowercase form.
	If -c is specified and added as an option, remove_case will be False and both lower and upper case letters 
	are added as a key. If -z option is passed, each letter of the alphabet will be printed, 
	regardless of whether that letter is contained in the file. '''

	# ioterating over each line of each file pasased
	for line in file:
		# iterating over each character in each line
		for char in line:
			# if the "remove_case" option is True, change every char to lowercase 
			if remove_case == True:
				char = char.lower()
			# checking whether the character is alpha, adding to dictionary and counting if so
			if char.isalpha() == True:
				if char in d:
					d[char] += 1
				else:
					d[char] = 1

# creating our main function to hold variables
def main():
	''' Our main() function holds all of our variables so that we dont declare them globally. Also
	calls our add_frequencies function. '''

	# defining our required and default variables
	d = {}
	argi = 1
	filenames = []
	case = True
	special_string = ''

	# iterating over arguments until we reach the first without "-", or the end of the list
	while argi < len(sys.argv):

		# assigning argument at current index to variable "arg"
		arg = sys.argv[argi]

		# breaking out of loop if argument starts with "-"
		if arg[0] != '-':
			break

		# handling the "-l" argument, passing the next argument as our special string
		# which will be the only characters we count
		if arg == '-l':
			special_string += sys.argv[argi+1]
			argi += 1

		# handling the "-c" argument, which determines count of upper and lowercase characters
		if arg == '-c':
			case = False

		# incrementing our index for the while loop
		argi += 1

	# interating over the files passed and adding each to the list from which we will count characters
	for name in sys.argv[argi:]:
		filenames.append(name)

	# handling our "-z" argument, whcih will determine whether we print the whole alphabet, even
	# if there is no count of the characters in the files we pass
	if ('-z' in sys.argv and '-c' in sys.argv):
		alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
		for let in alphabet:
			d[let] = 0
	elif '-z' in sys.argv:
		alphabet = 'abcdefghijklmnopqrstuvwxyz'
		for let in alphabet:
			d[let] = 0

	# calling our counting function
	for file in filenames:
		with open(file) as f: 
			add_frequencies(d, f, case)

	# second code block that handles our "-l" argument, determining which characters we count 
	# based on what is passed to the "special_string" variable
	for key, value in d.items():

		if '-l' in sys.argv:
			if key in special_string:
				print('%s,%d' % (key, value))
			else:
				print('%s,0' % (key))
		else:
			print('%s,%d' % (key, value))	

main()
