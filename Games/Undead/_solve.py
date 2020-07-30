import re, copy, enum

class Block(enum.Enum):
	EMPTY = 0
	MIRROR_LEFT = 1
	MIRROR_RIGHT = 2
	VAMPIRE = 3
	ZOMBIE = 4
	GHOST = 5
	def __eq__(self, value):
		return self.value == value

class Direction(enum.Enum):
	BOTTOM = 0
	LEFT = 1
	TOP = 2
	RIGHT = 3
	def __eq__(self, value):
		return self.value == value

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
	"""

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
		data = re.search(r'^(?P<w>[0-9]+)x(?P<h>[0-9]+):(?P<g>[0-9]+),(?P<v>[0-9]+),(?P<z>[0-9]+),(?P<mirrors>([a-z]?(R|L)[a-z]?)+),(?P<seen>([0-9],?)+)$', gameID)
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
				board._map[offset//board.Width][offset%board.Width] = Block.MIRROR_RIGHT.value if char == 'R' else Block.MIRROR_LEFT.value
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
		for (index, value) in enumerate(x for x in sum(self._map, []) if Block(x) in (Block.VAMPIRE, Block.ZOMBIE, Block.GHOST, Block.EMPTY)):
			output += 'V' if value == Block.VAMPIRE else ('Z' if value == Block.ZOMBIE else ('G' if value == Block.GHOST else 'N'))
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
		self.Vampires = board.Vampires - OneDBoardMap.count(Block.VAMPIRE.value)
		self.Ghosts = board.Ghosts - OneDBoardMap.count(Block.GHOST.value)
		self.Zombies = board.Zombies - OneDBoardMap.count(Block.ZOMBIE.value)

		if self.Vampires < 0 or self.Ghosts < 0 or self.Zombies < 0:
			raise ValueError("Board map have seted more monsters than is available.")
		elif self.Vampires + self.Ghosts + self.Zombies != OneDBoardMap.count(Block.EMPTY.value):
			raise ValueError("Board is invalid, count of free space is not equal monsters left to set.")

		self.Possible = dict()
		allAvailableMonsters = []
		if self.Vampires > 0:
			allAvailableMonsters.append(Block.VAMPIRE.value)
		if self.Zombies > 0:
			allAvailableMonsters.append(Block.ZOMBIE.value)
		if self.Ghosts > 0:
			allAvailableMonsters.append(Block.GHOST.value)

		for y in range(0, board.Height):
			for x in range(0, board.Width):
				if board._map[y][x] == Block.EMPTY:
					self.Possible[(x, y)] = copy.deepcopy(allAvailableMonsters)

	def getAllSeenBlocks(self, direction: Direction, axisValue: int) -> tuple:
		"""
		Method get all blocks seen from specifed direction and location on board.

		Parameters:
			direction (Direction): Direction define from you are looking.
			axisValue (int): Value of x on look axis.

		Returns:
			tuple: Tuple of tuples with location and status after first mirror. Schema: ((<x>, <y>, <0 if before first mirror else 1>), ...)
		"""
		assert type(direction) == Direction
		assert type(axisValue) == int and axisValue >= 0 and axisValue < (self.Board.Width if Direction(direction) in (Direction.TOP, Direction.BOTTOM) else self.Board.Height)

		blocks = []

		x = self.Board.Width-1 if direction == Direction.RIGHT else (0 if direction == Direction.LEFT else axisValue )
		y = self.Board.Height-1 if direction == Direction.BOTTOM else (0 if direction == Direction.TOP else axisValue )
		yInc = 1 if direction == Direction.TOP else (-1 if direction == Direction.BOTTOM else 0)
		xInc = 1 if direction == Direction.LEFT else (-1 if direction == Direction.RIGHT else 0)
		afterMirror = False

		while x in range(0, self.Board.Width) and y in range(0, self.Board.Height):
			if Block(self.Board._map[y][x]) in (Block.MIRROR_LEFT, Block.MIRROR_RIGHT):
				if xInc == 0:
					xInc, yInc = yInc, 0
				else:
					yInc, xInc = xInc, 0
				if Block(self.Board._map[y][x]) is Block.MIRROR_RIGHT:
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

	def setTo0Blocks(self):
		"""
		Method search way where are not any monster seen and set monsters.
		Returns:
			tuple: Blocks with monsters to set. Schema ((<x>, <y>, <MonsterID>), ...)
		"""
		zeroBlocks = []
		for direction, seenBoard in (
				(Direction.TOP, self.Board.SeenFromTop),
				(Direction.BOTTOM, self.Board.SeenFromBottom),
				(Direction.LEFT, self.Board.SeenFromLeft),
				(Direction.RIGHT, self.Board.SeenFromRight),
			):
			if 0 in seenBoard:
				for block_id, block in enumerate(seenBoard):
					if block == 0:
						zeroBlocks.append((direction, block_id))
		output = sum([list(self.getAllSeenBlocks(direction, axis)) for direction, axis in zeroBlocks], [])
		return tuple(set((b[0], b[1], Block.VAMPIRE.value if b[2] == 1 else Block.GHOST.value) for b in output))

	def setToLimitedBlocks(self):
		"""
		Method search ways were count of seen blocks is greater than seen blocks, and count of already set monsters.
		If recalculated count of seen monster is equal 0 or length of seen blocks, then create changes for Possible.
		Returns:
			tuple: Blocks with possible monsters to set. Schema ((<x>, <y>, {<MonsterID>, ...}), ...)
		"""
		data = []
		for direction, seenBoard in (
				(Direction.TOP, self.Board.SeenFromTop),
				(Direction.BOTTOM, self.Board.SeenFromBottom),
				(Direction.LEFT, self.Board.SeenFromLeft),
				(Direction.RIGHT, self.Board.SeenFromRight),
			):
			for x, seen in enumerate(seenBoard):
				seenBlocks = list(self.getAllSeenBlocks(direction, x))
				for block in seenBlocks:
					blockType = Block(self.Board._map[block[1]][block[0]])
					if blockType is not Block.EMPTY:
						if block[2] == 0:
							if blockType in (Block.ZOMBIE, Block.VAMPIRE):
								seen -= 1
						elif blockType in (Block.ZOMBIE, Block.GHOST):
							seen -= 1
						seenBlocks.remove(block)
				if seen == 0:
					for x in seenBlocks:
						data.append((x[0], x[1], [Block.GHOST.value if x[2] == 0 else Block.VAMPIRE.value]))
				elif seen == len(seenBlocks):
					for x in seenBlocks:
						data.append((x[0], x[1], [Block.ZOMBIE.value, Block.GHOST.value if x[2] == 1 else Block.VAMPIRE.value]))
		output = []
		for d in data:
			possible = set(d[2])
			similarBlocks = [x for x in data if (x[0], x[1]) == (d[0], d[1])]
			for similar in similarBlocks:
				possible &= set(similar[2])
				data.remove(similar)
			output.append((d[0], d[1], set(possible)))
		return tuple(output)








