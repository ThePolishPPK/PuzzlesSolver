import re

class Board:
	"""
	Class store information about monsters type, mirrors, count of seen monsters and count of every type of monster.

	Attributes:
		Width (int): Count of columns.
		Height (int): Count of rows.
		Vampires (int): Count of Vampires.
		Zombies (int): Count of Zombies.
		Ghosts (int): Count of Ghosts.
		SeenFromTop (tuple): Tuple of ints containing count of seen monsters from top on specific column.
		SeenFromBottom (tuple): Tuple of ints containing count of seen monsters from bottom on specific column.
		SeenFromLeft (tuple): Tuple of ints containing count of seen monsters from left on specific row.
		SeenFromRight (tuple): Tuple of ints containing count of seen monsters from right on specific row.
		_map (list): List of rows with ints defining specific element on board.

	BoardElements:
		0 - Empty
		1 - Mirror (Left)	(\)
		2 - Mirror (Right)	(/)
		3 - Vampire
		4 - Zombie
		5 - Ghost
	"""
	EMPTY = 0
	MIRROR_LEFT = 1
	MIRROR_RIGHT = 2
	VAMPIRE = 3
	ZOMBIE = 4
	GHOST = 5

	def __init__(self, width: int, height: int) -> None:
		"""
		Constructor for Board class.

		Parameters:
			width (int): Count of columns.
			height (int): Count of rows.
		"""
		self.Width = width
		self.Height = height
		self.Vampires = 0
		self.Zombies = 0
		self.Ghosts = 0
		self.SeenFromTop = ()
		self.SeenFromBottom= ()
		self.SeenFromLeft = ()
		self.SeenFromRight = ()
		self._map = [[0]*width for _ in range(0, height) ]

	@classmethod
	def parseGameID(cls, gameID: str) -> 'Board':
		"""
		Method parse data from gameID and create Board object based on recived data.

		Parameters:
			gameID (str): Game ID string.

		Returns:
			Board: Board object.
		"""
		data = re.search(r'^(?P<w>[0-9]+)x(?P<h>[0-9]+):(?P<g>[0-9]+),(?P<v>[0-9]+),(?P<z>[0-9]+),(?P<mirrors>((R|L)[a-z]?)+),(?P<seen>([0-9],?)+)$', gameID)
		board = cls(int(data.group('w')), int(data.group('h')))
		board.Ghosts = int(data.group('g'))
		board.Vampires = int(data.group('v'))
		board.Zombies = int(data.group('z'))

		seen = [int(x) for x in data.group('seen').split(',')]
		board.SeenFromTop = tuple(seen[0:board.Width])
		board.SeenFromRight = tuple(seen[board.Width:board.Width+board.Height])
		board.SeenFromBottom = tuple(seen[board.Width+board.Height:(2*board.Width)+board.Height][::-1])
		board.SeenFromLeft = tuple(seen[(2*board.Width)+board.Height:(2*(board.Width+board.Height))][::-1])

		offset = 0
		for char in data.group('mirrors'):
			if char in ('R', 'L'):
				board._map[offset//board.Width][offset%board.Width] = Board.MIRROR_RIGHT if char == 'R' else Board.MIRROR_LEFT
				offset += 1
			else:
				offset += ord(char)-96
				if offset/board.Width >= board.Height:
					break

		return board

	def exportToSolveFormat(self) -> str:
		"""
		Method parse some data from solved board to solve string:

		Returns:
			str: Solve string.
		"""
		output = " "
		for (index, value) in enumerate(x for x in sum(self._map, []) if x in (Board.VAMPIRE, Board.ZOMBIE, Board.GHOST, Board.EMPTY)):
			output += 'V' if value == Board.VAMPIRE else ('Z' if value == Board.ZOMBIE else ('G' if value == Board.GHOST else 'N'))
			output += str(index+1)
			output += ";"
		return output[1:-1]

	def copy(self) -> 'Board':
		"""
		Method make copy of Board object.

		Returns:
			Board: Copied Board object.
		"""
		board = Board(self.Width, self.Height)
		board._map = copy.deepcopy(self._map)
		board.Vampires = self.Vampires
		board.Zombies = self.Zombies
		board.Ghosts = self.Ghosts
		board.SeenFromTop = copy.deepcopy(self.SeenFromTop)
		board.SeenFromBottom = copy.deepcopy(self.SeenFromBottom)
		board.SeenFromLeft = copy.deepcopy(self.SeenFromLeft)
		board.SeenFromRight = copy.deepcopy(self.SeenFromRight)
		return board