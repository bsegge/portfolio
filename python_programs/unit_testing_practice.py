## Brian Seggebruch - 873408239 - program to encode and decode strings
## into and from pylatin

## importing used modules
import string
import unittest

## defining global variables
vowels = 'aeiouyAEIOUY'
consonants = ''.join(letter for letter in string.ascii_letters
					if letter
					not in vowels)


def to_pylatin(s):
	'''Takes a string and converts it to "pylatin". If the string is
	less than 3 characters, it returns the string unchanged.'''

	## raising error if a non-string is passed
	if type(s) != str:
		raise TypeError

	## iterating over characters in string and raising error if not
	## in ascii letters
	for char in s:
		if char not in string.ascii_letters:
			raise ValueError

	## returning string unchanged if length less than 3
	if len(s) < 3:
		return s

	## handling strings that begin with consonants
	elif s[0] in consonants:
		cons_string = ''
		for idx, char in enumerate(s):
			if char in vowels:
				vowel_idx = idx
				break
			else:
				cons_string += char
		new_string = s[vowel_idx:] + 'py'
		return new_string + cons_string

	## handling strings that begin with vowels
	elif s[0] in vowels:
		vowel_string = ''
		for idx, char in enumerate(s):
			if char in consonants:
				cons_idx = idx
				break
			else:
				vowel_string += char
		new_string = s[cons_idx:] + 'on'
		return new_string + vowel_string

def from_pylatin(s):
	'''Takes a pylatin string and converts it back to its original form'''

	## raising error if a non-string is passed
	if type(s) != str:
		raise TypeError

	## iterating over characters in string and raising error if not
	## in ascii letters
	for char in s:
		if char not in string.ascii_letters:
			raise ValueError

	## returning string unchanged if length less than 3
	if len(s) < 3:
		return s

	## handling strings that end with consonants
	elif s[-1] in consonants:
		if 'py' not in s:
			raise ValueError
		else:
			holdme = s.rsplit('py', maxsplit = 1)
			# print(holdme)
			for letter in holdme[1]:
				if letter in vowels:
					raise ValueError
			return holdme[1]+holdme[0]

	## handling strings that end with vowels
	elif s[-1] in vowels:
		if 'on' not in s:
			raise ValueError
		else:
			holdme = s.rsplit('on', maxsplit = 1)
			# print(holdme)
			for letter in holdme[1]:
				if letter in consonants:
					raise ValueError
			return holdme[1]+holdme[0]


class testpylatin(unittest.TestCase):
	'''Tests our functions with various parameters and configurations'''

	improper_len_strings = [
	('it'),
	('he'),
	('is'),
	('at'),
	('on'),
	('py')
	]

	bad_char = [
	('h3llo'),
	('Gr8'),
	('Alameda"'),
	('!@)@#^%(*&')
	]

	pylayin_strings = [
	('ellopyh','hello')
	,('ENveRpyd','dENveR')
	,('ythonpyp','python')
	,('ylonpyp','pylon')
	,('oughpyth','though')
	,('enverpyD','Denver')
	,('valononA','Avalon')
	,('rdinaryono','ordinary')
	,('wFulona','awFul')
	,('ndona','and')
	]

	non_pylatin_strings = [
	('asdfpyasd'),
	('asdfondfi'),
	('python'),
	('pylon'),
	('crockpot'),
	('Kombucha')
	]

	pre_pylatin_strings = [
	('though','oughpyth')
	,('THough','oughpyTH')
	,('Denver','enverpyD')
	,('Avalon','valononA')
	,('Pylon','ylonpyP')
	,('ordinary','rdinaryono')
	,('awFul','wFulona')
	,('and','ndona')
	,('onononon','nonononono')
	]

	## test to ensure string is of string type
	def test_bad_strings(self):
		for bad_string in [12, True, [], {}, 0.5]:
			with self.subTest(bad_string = bad_string):
				with self.assertRaises(TypeError):
					s_to = to_pylatin(bad_string)
					s_from = from_pylatin(bad_string)

	## test to ensure length of string is handled properly
	def test_proper_length(self):
		for string in self.improper_len_strings:
			with self.subTest(string = string):
				result_s_to = to_pylatin(string)
				result_s_from = from_pylatin(string)
				self.assertEqual(result_s_to, string)
				self.assertEqual(result_s_from, string)

	## test to esnure there are no non-letters in the string
	def test_proper_char(self):
		for string in self.bad_char:
			with self.subTest(bad_char = string):
				with self.assertRaises(ValueError):
					s_to = to_pylatin(string)
					s_from = from_pylatin(string)

	## test that the string passed to from_pylatin is actually a pylatin string
	def test_non_pylatin(self):
		for string in self.non_pylatin_strings:
			with self.subTest(non_pylatin_string = string):
				with self.assertRaises(ValueError):
					s = from_pylatin(string)

	## test the from_pylatin function to ensure it returns as expected
	def test_from_pylatin(self):
		for before, after in self.pylayin_strings:
			with self.subTest(pylatin_string = after):
				s = from_pylatin(before)
				self.assertEqual(s, after)

	## test the to_pylatin function to ensure it returns as expected
	def test_to_pylatin(self):
		for before, after in self.pre_pylatin_strings:
			with self.subTest(pylatin_string = after):
				s = to_pylatin(before)
				self.assertEqual(s, after)

if __name__ == '__main__':
	unittest.main()
