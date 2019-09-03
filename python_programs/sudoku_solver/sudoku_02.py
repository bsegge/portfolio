# Brian Seggebruch - 873408239 - Sudoku solving program

import sys
from itertools import chain

class Puzzle:
	'''Creates Puzzle object that takes a list of 6 lists with
	6 integers between 1 and 6 each, builds a sudoku puzzle,
	and solves it.'''

	def __init__(self, board):

		## checking that the appropriate list of lists 
		## is passed to our Puzzle class
		if len(board) < 6:
			raise ValueError ('len of first list less than 6')
		elif type(board) != list:
			raise ValueError ('the board you passed is not a list')
		elif any(type(nested_li) != list for nested_li in board):
			raise ValueError ('something in the board is not a list')
		elif any(len(nested_li) != 6 for nested_li in board):
			raise ValueError ('something in the board does not have 6 characters')
		elif any(type(nested_li[i]) != int for nested_li in board for i in range(len(nested_li))):
			raise ValueError ('something in the board is not an integer')
		elif any(i < 0 or i > 6 for nested_li in board for i in nested_li):
			raise ValueError ('one of the integers in the board is not between 0 and 6')

		## creates a deep copy of the passed parameter
		else:
			self.board = list( a[:] for a in board )

	def __str__(self):
		'''create and prints the sudoku puzzle'''

		## setting up our string to print
		ending_str = ''

		## iterating over each list in our board
		for nested_li in self.board:
			print_line = ''	
			## adding characters for the first 3 columns		
			for char in nested_li[:3]:
				## replacing 0's with '_'
				if char == 0:
					print_line += '_'
				else:
					print_line += str(char)
				## adding space to end of each character
				print_line += ' '
			## adding space between 3 columns on either side
			print_line += ' '

			## adding characters for last 3 columns
			for char in nested_li[3:]:
				if char == 0:
					print_line += '_'
				else:
					print_line += str(char)
				print_line += ' '
			## adding new line at the end of each row
			print_line += '\n'
			## building our final printable
			ending_str += print_line
			
		return(ending_str)

	def options(self, row, col):
		'''returns the possible solutions for the
		given space within the sudoku puzzle'''

		## setting up containers to track our blocks,
		## rows, and columns
		block_current = {}
		row_current = {}
		col_current = {}

		## defining the upper left index of each block
		upper_left = []
		for r in [0,2,4]:
			for c in [0,3]:
				upper_left.append((r,c))

		## creating list with values in order of each block
		blocks = []
		for corner in upper_left:
			for row_idx in range(corner[0],corner[0]+2):
				for col_idx	in range(corner[1], corner[1]+3):
					blocks.append(self.board[row_idx][col_idx])

		## adding the appropriate 6 values to each block variable
		for block_idx in range(6):
			block_current[block_idx] = []
			block_current[block_idx].append(
				blocks[block_idx*6:(block_idx*6+6)]
		 		)				

		## setting up column variables
		for i in range(6):
			col_current[i] = []

		## adding values to our row and column variables
		for i in range(6):
			row_current[i] = self.board[i]
			for j in range(6):
				col_current[j].append(self.board[i][j])

		## setting up to analyze solutions to given space
		sq = self.board[row][col]
		options_set = set()
		block_num = 0

		## defining our block number (if not 0)
		if col < 3:
			if row in (2,3):
				block_num = 2
			elif row in (4,5):
				block_num = 4
		else:
			if row in (0,1):
				block_num = 1
			elif row in (2,3):
				block_num = 3
			else:
				block_num = 5

		## if the current space is 0, add the right value(s) to
		## the set of possible solutions
		if sq == 0:
			for i in range(1,7):
				if i not in block_current[block_num][0]	\
				 and i not in row_current[row]	\
				 and i not in col_current[col]:
					options_set.add(i)

			return options_set
		else:
			return options_set

	def solve(self):
		'''recursively solves our sudoku puzzle'''

		print(self)

		## if no 0's remain, puzzle solved
		if 0 not in list(chain(*self.board)):
			return True

		## recursively iterate through possible solutions
		for li_idx, li in enumerate(self.board):
			for idx, sq in enumerate(li):
				if self.board[li_idx][idx] == 0:
					valid_options = self.options(li_idx,idx)
					for opt in valid_options:
						self.board[li_idx][idx] = opt
						if self.solve():
							return True
					self.board[li_idx][idx] = 0
					return False


def main():

	filenames = []
	argi = 1
	derived_board = []

	## adding files to our list of files
	for name in sys.argv[argi:]:
		filenames.append(name)

	## for each file, convert to puzzle object and solve
	for file in filenames:
		with open(file) as f: 
			for line in f:
				line_li = []
				for char in line:
					if char != ' ' and char != '\n':
						line_li.append(int(char))
				derived_board.append(line_li)
		sudoku = Puzzle(derived_board)
		sudoku.solve()

if __name__ == '__main__':
	main()