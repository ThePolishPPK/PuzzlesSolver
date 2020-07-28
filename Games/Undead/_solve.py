import re, copy

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

class Solve:
	"""
	Class contain all method required to solve and solve gived board.

	Attributes:
		Board (Board): Board object containing map to solve.
		Possible (dict): Dict of possible monsters to set on block. Schema: {(<x>,<y>): [<Vampire>/<Ghost>/<Zombie>], ...}
		Vampires (int): Count of Vampires left to set.
		Ghosts (int): Count of Ghosts left to set.
		Zombies (int): Count of Zombies left to set.
	"""
	def __init__(self, board: Board) -> None:
		"""
		Constructor for class.

		Parameters:
			board (Board): Board object with map to solve.
		"""
		assert type(board) is Board and [len(y) for y in board._map].count(board.Width) == board.Height

		self.Board = board
		OneDBoardMap = sum(board._map, [])
		self.Vampires = board.Vampires - OneDBoardMap.count(Board.VAMPIRE)
		self.Ghosts = board.Ghosts - OneDBoardMap.count(Board.GHOST)
		self.Zombies = board.Zombies - OneDBoardMap.count(Board.ZOMBIE)

		if self.Vampires < 0 or self.Ghosts < 0 or self.Zombies < 0:
			raise ValueError("Board map have seted more monsters than is available.")
		elif self.Vampires + self.Ghosts + self.Zombies != OneDBoardMap.count(Board.EMPTY):
			raise ValueError("Board is invalid, count of free space is not equal monsters left to set.")

		self.Possible = dict()
		allAvailableMonsters = []
		if self.Vampires > 0:
			allAvailableMonsters.append(Board.VAMPIRE)
		if self.Zombies > 0:
			allAvailableMonsters.append(Board.ZOMBIE)
		if self.Ghosts > 0:
			allAvailableMonsters.append(Board.GHOST)

		for y in range(0, board.Height):
			for x in range(0, board.Width):
				if board._map[y][x] is Board.EMPTY:
					self.Possible = copy.deepcopy(allAvailableMonsters)

	def getAllSeenBlocks(self, direction: int, axisValue: int) -> tuple:
		"""
		Method get all blocks seen from specifed direction and location on board.

		Parameters:
			direction (int): Direction define from you are looking.
			axisValue (int): Value of x on look axis.

		Returns:
			tuple: Tuple of tuples with location and status after first mirror. Schema: ((<x>, <y>, <0 if before first mirror else 1>), ...)

		Directions:
			0 - From Top to Bottom
			1 - From Right to Left
			2 - From Bottom to Top
			3 - From Left to Right
		"""
		assert type(direction) == int and direction >= 0 and direction <= 3
		assert type(axisValue) == int and axisValue >= 0 and axisValue < (self.Board.Width if direction in (2, 0) else self.Board.Height)

		blocks = []

		x = self.Board.Width-1 if direction == 1 else (0 if direction == 3 else axisValue )
		y = self.Board.Height-1 if direction == 2 else (0 if direction == 0 else axisValue )
		xInc = 1 if direction == 3 else (-1 if direction == 1 else 0)
		yInc = 1 if direction == 0 else (-1 if direction == 2 else 0)
		afterMirror = False

		while x in range(0, self.Board.Width) and y in range(0, self.Board.Height):
			if self.Board._map[y][x] in (Board.MIRROR_LEFT, Board.MIRROR_RIGHT):
				if xInc == 0:
					xInc, yInc = yInc, 0
				else:
					yInc, xInc = xInc, 0
				if self.Board._map[y][x] is Board.MIRROR_RIGHT:
					if yInc == 0:
						xInc *= -1
					else:
						yInc *= -1
				afterMirror = True
			else:
				blocks.append((x, y, 1 if afterMirror else 0))
			x += xInc
			y += yInc
		return tuple(blocks)














