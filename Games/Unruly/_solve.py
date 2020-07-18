import re

class Board:
	"""
	Class containing data about board and blocks on them.

	Attributes:
		_map (list): 2D list matrix contains Block objects.
		Width (int): Count of blocks in X axis.
		Height (int): Count of blocks in Y axis.
		UniqueInX (int): Count of one color blocks in row.
		UniqueInY (int): Count of one color blocks in column.
		UniqueRowsAndColumns (bool): Define in rules to check rows and columns.
	"""
	def __init__(self, width: int, height: int, uniqueInX: int = None, uniqueInY: int = None, uniqueRowsAndColumns: bool = False) -> None:
		"""
		Constructor for Board class.

		Parameters:
			width (int): Board width.
			height (int): Board height.
			uniqueInX (int): Count of block one color in row. (default: width//2)
			uniqueInY (int): Count of block one color in column. (default: height//2)
			uniqueRowsAndColumns (bool): Rule config, define checking unique rows and columns. (default: False)
		"""
		self.Width = width
		self.Height = height
		self.UniqueInX = uniqueInX if type(uniqueInX) == int else self.Width // 2
		self.UniqueInY = uniqueInY if type(uniqueInY) == int else self.Height // 2
		self.UniqueRowsAndColumns = uniqueRowsAndColumns
		self._map = [ [None]*self.Width for _ in range(self.Height) ]

	@classmethod
	def parse(cls, data: str) -> 'Board':
		"""
		Method detect type of data and create Board object if it's possible.

		Parameters:
			data (str): Board map data.

		Returns:
			Board: Board with map created by data parameter.
		"""
		if re.search(r"^[0-9]+x[0-9]+:[a-zA-Z]+$", data) is not None:
			return cls._parseGameID(data)

	@classmethod
	def _parseGameID(cls, gameID: str) -> 'Board':
		"""
		Method parse inputed gameID and create Board object with map defined by data.

		Parameters:
			gameID (str): Data about map saved in specifed (by author) GameID style.

		Returns:
			Board: Board object with map defined by gameID parameter.
		"""
		data = re.search(r"^(?P<w>[0-9]+)x(?P<h>[0-9]+):(?P<GID>[a-zA-Z]+)$", gameID)
		board = cls(
			int(data.group("w")),
			int(data.group("h"))
		)
		offset = -1
		for char in data.group("GID"):
			blockType = Block.BLACK if char == char.upper() else Block.WHITE
			offset += ord(char.upper()) - 64

			if offset >= board.Width * board.Height:
				break

			block = Block(
				x=offset % board.Width,
				y=offset // board.Width,
				blockType=blockType
			)
			board._map[block.y][block.x] = block

		for x, y in ((x,y) for x in range(board.Width) for y in range(board.Height)):
			if board._map[y][x] is None:
				board._map[y][x] = Block(
					x=x,
					y=y,
					blockType=Block.EMPTY
				)

		return board

	def exportToGameID(self) -> str:
		"""
		Method parse data to GameID string.

		Returns:
			str: GameID Data.
		"""
		gameID = ""
		offset = 0
		for y in range(self.Height):
			for x in range(self.Width):
				if self._map[y][x].Type != Block.EMPTY:
					char = chr(offset+65)
					gameID += char.lower() if self._map[y][x].Type == Block.WHITE else char.upper()
					offset = 0
				else:
					offset += 1
		gameID += chr(offset + 97)
		return "{}x{}:{}".format(
			str(self.Width),
			str(self.Height),
			gameID
		)

	def exportToBinaryMatrix(self) -> list:
		"""
		Method create 2D matrix and fill them with 0, 1 and None values.
		0 - White
		1 - Black
		None - Empty

		Returns:
			list: 2D matrix with blocks types.
		"""
		board = [[None]*self.Width for _ in range(self.Height)]
		for x,y in ((x,y) for x in range(self.Width) for y in range(self.Height)):
			if self._map[y][x].Type != Block.EMPTY:
				board[y][x] = 0 if self._map[y][x].Type == Block.WHITE else 1
		return board

	def isValid(self) -> bool:
		"""
		Method check Board with game rules.

		Returns:
			bool: True if board is valid else False
		"""
		board = self.exportToBinaryMatrix()

		# Check block counts in row
		for y in range(self.Height):
			if (board[y].count(1) > self.UniqueInX or
				board[y].count(0) > self.UniqueInX):
				return False

		# Check block counts in column
		for y in ([board[y][x] for y in range(self.Height)] for x in range(self.Width)):
			if (y.count(1) > self.UniqueInY or
				y.count(0) > self.UniqueInY):
				return False

		if self.UniqueRowsAndColumns:
			for row in (x for x in board if None not in board):
				if board.count(row) > 1:
					return False
			columns = list([board[y][x] for y in range(self.Height)] for x in range(self.Width))
			for column in (y for y in columns if None not in y):
				if columns.count(column) > 1:
					return False
		return True

	def copy(self) -> 'Board':
		"""
		Method make copy of Board object.

		Returns:
			Board: Cloned Board object.
		"""
		board = Board(
			self.Width,
			self.Height,
			self.UniqueInX,
			self.UniqueInY
		)
		for x, y in ((x,y) for x in range(self.Width) for y in range(self.Height)):
			board._map[y][x] = Block(
				x=x,
				y=y,
				blockType=self._map[y][x].Type
			)

		return board

	def __getitem__(self, location: tuple) -> 'Block':
		if (location[0] not in range(self.Width)
			or location[1] not in range(self.Height)):
			raise IndexError("That block doesn't exist!")
		else:
			return self._map[location[1]][location[0]]

class Block:
	"""
	Class contaion information about block location and type.

	Attributes:
		x (int): X coordinate value of block location on x axis.
		y (int): Y coordinate value of block location on y axis.
		Type (int): Integer value representing type of block.
		EMPTY (int): Static value for empty block type.
		WHITE (int): Static value for white block type.
		BLACK (int): Static value for black block type.
	"""

	EMPTY = 0
	WHITE = 1
	BLACK = 2

	def __init__(self, x: int, y: int, blockType: int = 0) -> None:
		"""
		Constructor for Block class.

		Parameters:
			x (int): Block location on x axis.
			y (int): Block location on y axis.
			blockType (int): Block type. (default: 0)
		"""
		self.x = x
		self.y = y
		self.Type = blockType

	def __repr__(self) -> str:
		return "<Block Type={} x={} y={}>".format(
			"Black" if self.Type == Block.BLACK else ("WHITE" if self.Type == Block.WHITE else ("EMPTY" if self.Type == Block.EMPTY else "undefined")),
			self.x,
			self.y
		)


class Solve:
	"""
	Class make all algorithm steps to solve board.
	"""
	def __init__(self, board: Board) -> None:
		"""
		Constructor for 'Solve' class.

		Parameters:
			board (Board): Board object what shoud be solved.
		"""
		pass

	def solve(self) -> list:
		"""
		Method solve board and create binary matrix representing color of every block.

		Returns:
			list: 2D matrix with ints representing blocks color: 0 - White, 1 - Black.
		"""
		pass

	def addWallsForDublesInLine(self) -> list:
		"""
		Method search dubled blocks in one color and check existing his ways.

		Returns:
			list: List of coordinates where shoud be seted blocks and them color eg. [(3,5,0),(5,6,1)]
		"""
		pass

	def checkOutOfBlockOneColorInLine(self) -> list:
		"""
		Method count blocks in line and check limits. If count of blocks are end, then other empty blocks fill with second color.

		Returns:
			list: List of coordinates where shoud be seted blocks and them color eg. [(3,5,0),(5,6,1)]
		"""
		pass

	def checkEmptyBlockBetweenTwoInLine(self) -> list:
		"""
		Method search two blocks in line with this same color and one empty block between them.

		Returns:
			list: List of coordinates where shoud be seted blocks and them color eg. [(3,5,0),(5,6,1)]
		"""
		pass

	def radomizeOneBlock(self) -> 'Board':
		"""
		Method clone Board and set random block with random color.

		Returns:
			Board: Board object with correct blocks.
		"""
		pass
