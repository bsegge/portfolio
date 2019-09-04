## Brian Seggebruch -- 873408239 -- program to iterate over unique permutations

import unittest
from math import factorial

class MSPermutations:
	'''Iterable class that returns all the unique permutations of a 
	given collection.'''

	def __init__(self, collection):
		self.collection = collection

	def __iter__(self):
		# printing first, sorted tuple, then using iterator
		return MSPIterator(self.collection)

class MSPIterator:
	'''An iterator class that that iterates over all unique permutations
	of a given collection.'''

	def __init__(self, collection):
		self.collection = tuple(sorted(collection))
		self.next_permutation = self.collection
		# there should be factorial(collection) number of permutations
		self.limit = factorial(len(collection))
		self.limit_idx = 0

	def __iter__(self):
		return self

	def __next__(self):

		if len(self.collection) == 0:
			raise StopIteration

		# stopping when we have the right number of values returned
		while self.limit_idx < self.limit:
			# iterating until sorted in descending order
			current_permutation = self.next_permutation
			if any(self.collection[i] < self.collection[i+1] for i in range(0, len(self.collection)-1)):
				try:
					# finding i and j
					idx = len(self.collection) - 2
					while idx >= 0:
						if self.collection[idx] < self.collection[idx+1]:
							i = idx
							idx = -1
						else:
							idx -= 1

					idx = len(self.collection) - 1
					while idx > i:
						if self.collection[idx] > self.collection[i]:
							j = idx
							idx = i
						else:
							idx -= 1	

					# prepping to swap i and j
					self.collection = list(self.collection)
					temp_i = self.collection[i]
					temp_j = self.collection[j]

					# swapping i and j
					self.collection[i] = temp_j
					self.collection[j] = temp_i
					# reversing ending and returning
					self.collection = self.collection[0:i+1] + self.collection[:i:-1]
					self.next_permutation = tuple(self.collection)

					self.limit_idx += 1
					return current_permutation

				except:
					self.limit_idx += 1
					return

			else:
				self.limit_idx += 1
				# return our last made permutation
				return current_permutation

		raise StopIteration

def unique_permutations(collection):
	'''Creates a generator that can be used to iterate over all unique permutations
	of the given collection.'''

	collection = tuple(sorted(collection))
	switch = True

	if len(collection) == 0:
		return

	# yielding our first, sorted tuple
	yield tuple(collection)

	# looping until switch is flipped
	while switch == True:
		try:
			# finding i and j
			idx = len(collection) - 2
			while idx >= 0:
				if collection[idx] < collection[idx+1]:
					i = idx
					idx = -1
				else:
					idx -= 1

			idx = len(collection) - 1
			while idx > i:
				if collection[idx] > collection[i]:
					j = idx
					idx = i
				else:
					idx -= 1	

			# prepping to swap i and j
			collection = list(collection)
			temp_i = collection[i]
			temp_j = collection[j]

			# swapping i and j
			collection[i] = temp_j
			collection[j] = temp_i
			# reversing ending and yielding
			collection = collection[0:i+1] + collection[:i:-1]
			yield tuple(collection)

			# flip switch if there is no i such that... 
			# ... collection[i] < collection[i+1]
			if any(collection[i] < collection[i+1] for i in range(0, len(collection)-1)):
				switch = True
			else:
				switch = False
		except:
			return

class testPermutations(unittest.TestCase):
	'''Tests our functions with various parameters and configurations'''

	before_after = [
	([1,1,1], [(1,1,1)])
	,([2,1,1], [(1,1,2), (1,2,1), (2,1,1)])
	,(['a', 'b', 'a'], [('a','a','b'), ('a','b','a'), ('b','a','a')])
	,({'these', 'are', 'words'}, [('are', 'these', 'words'),
								('are', 'words', 'these'),
								('these', 'are', 'words'),
								('these', 'words', 'are'),
								('words', 'are', 'these'),
								('words', 'these', 'are')])
	]

	# test the unique_permutations function to ensure it returns as expected
	def test_output(self):
		for before, after in self.before_after:
			with self.subTest(output = after):
				output_tuples = []
				for i in unique_permutations(before):
					output_tuples.append(i)
				self.assertEqual(output_tuples, after)

if __name__ == '__main__':
	unittest.main()