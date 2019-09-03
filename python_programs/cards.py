## Brian Seggebruch -- 873408239 -- game of war program

import string
import random
import sys


class Card:
	'''Has two attributes, rank and suit, which are selected from the 
	same collection of ranks and suits of a standard deck of playing cards.
	Has the functionality to compare card objects based on rank.'''

	RANKS = ['Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten'
			, 'Jack', 'Queen', 'King', 'Ace']
	SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
	
	def __init__(self, rank, suit):

		# checking types and values of our ranks/suits	
		if type(rank) == str:
			if rank.lower() in [i.lower() for i in self.RANKS]:
				self.rank = rank.lower()
			else:
				raise ValueError ('the rank you gave is not a proper rank')
		else:
			raise ValueError ('the rank you gave is not of type string')
		if type(suit) == str:
			if suit.lower() in [i.lower() for i in self.SUITS]:
				self.suit = suit.lower()
			else:
				raise ValueError ('the suit you gave is not a proper suit')
		else:
			raise ValueError ('the suit you gave is not of type string')
	
	# returns a readable version of our object		
	def __str__(self):
		return f'{self.rank} of {self.suit}'
		
	# returns a string that can be used to create the object
	def __repr__(self):
		return f'Card({self.rank!r}, {self.suit!r})'

	# allows our object to be hashable
	def __hash__(self):
		return hash(self.rank, self.suit)
		
	## functionality to compare values of our objects
	def __eq__(self, other):
		if type(self) == type(other):
			return ((self.rank)
					== (other.rank))
		else:
			return NotImplemented
			
	def __ne__(self, other):
		return not self.__eq__(other)
	
	def __lt__(self, other):
		if type(self) == type(other):
			for idx, r in enumerate([i.lower() for i in self.RANKS]):
				if self.rank == r:
					s_idx = idx
				if other.rank == r:
					o_idx = idx
			return (s_idx < o_idx)
		else:
			return NotImplemented	
	
	def __gt__(self, other):
		if type(self) == type(other):
			for idx, r in enumerate([i.lower() for i in self.RANKS]):
				if self.rank == r:
					s_idx = idx
				if other.rank == r:
					o_idx = idx
			return (s_idx > o_idx)
		else:
			return NotImplemented	

	def __le__(self, other):
		if type(self) == type(other):
			for idx, r in enumerate([i.lower() for i in self.RANKS]):
				if self.rank == r:
					s_idx = idx
				if other.rank == r:
					o_idx = idx
			return (s_idx <= o_idx)
		else:
			return NotImplemented

	def __ge__(self, other):
		if type(self) == type(other):
			for idx, r in enumerate([i.lower() for i in self.RANKS]):
				if self.rank == r:
					s_idx = idx
				if other.rank == r:
					o_idx = idx
			return (s_idx >= o_idx)
		else:
			return NotImplemented
			
	
def standard_deck(cls):
	'''A standard deck of 52 cards, each with a unique rank/suit combo'''
	deck = []

	# creating an object for each combination
	for i in cls.RANKS:
		for j in cls.SUITS:
			deck.append(cls(i, j))
	return deck
	
def simulate_war(deck, max_turns):
	'''Simulates a game of "war", where two players each get half a standard
	deck of cards, and compare  the top card. The simulation ends when a player
	runs out of cards, or tha max_turns parameter is reached.'''
	turn = 0
	trick = []
	war_deck = deck

	random.shuffle(war_deck)

	player_1_hand = war_deck[0:26]
	player_2_hand = war_deck[26:]

	# looping until one player runs out of cards
	while all([player_1_hand, player_2_hand]):
		# ending if we run out of turns
		if turn < max_turns:
			## comparing value of cards and moving the cards
			## per the rules of the game
			if player_1_hand[0] > player_2_hand[0]:
				[trick.append(c) for c in [player_1_hand[0]]+[player_2_hand[0]]]
				player_1_hand = player_1_hand[1:]
				player_2_hand = player_2_hand[1:]
				[player_1_hand.append(i) for i in trick]
				trick = []

			elif player_1_hand[0] == player_2_hand[0]:
				[trick.append(c) for c in player_1_hand[0:3]+player_2_hand[0:3]]
				player_1_hand = player_1_hand[3:]
				player_2_hand = player_2_hand[3:]
				
			else:
				[trick.append(c) for c in [player_1_hand[0]]+[player_2_hand[0]]]
				player_1_hand = player_1_hand[1:]
				player_2_hand = player_2_hand[1:]
				[player_2_hand.append(i) for i in trick]
				trick = []
							
			turn += 1
		else:
			return max_turns
		
	
	return turn
	
def main():
	
	# defining defaults
	trials = 1
	max_turns = 5000
	argi = 1
	
	# looking for options passed
	while argi < len(sys.argv):

		arg = sys.argv[argi]

		if arg[0] != '-':
			break

		# specifying the number of days
		elif arg == '-t':
			trials = int(sys.argv[argi+1])
			argi += 1

		# specifying the number of trials
		elif arg == '-m':
			max_turns = int(sys.argv[argi+1])
			argi += 1

		else:
			print(f"unrecognized argument: {arg}")

		argi += 1
	
	# running our simulation [trial] times		
	for i in range(trials):
		deck = standard_deck(Card)
		print(simulate_war(deck, max_turns))
		
		
if __name__ == '__main__':
	main()
	
	
	
	
	
	
	
	