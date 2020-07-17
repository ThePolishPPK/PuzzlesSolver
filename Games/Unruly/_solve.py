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
	"""
	def __init__(self, width: int, height: int, uniqueInX: int = None, uniqueInY: int = None) -> None:
		"""
		Constructor for Board class.

		Parameters:
			width (int): Board width.
			height (int): Board height.
			uniqueInX (int): Count of block one color in row. (default: width//2)
			uniqueInY (int): Count of block one color in column. (default: height//2)
		"""
		self.Width = width
		self.Height = height
		self.UniqueInX = uniqueInX if type(uniqueInX) == int else self.Width // 2
		self.UniqueInY = uniqueInY if type(uniqueInY) == int else self.Height // 2
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
					gameID = char.lower() if self._map[y][x].Type == Block.WHITE else char.upper()
					offset = 0
				else:
					offset += 1
		return "{}x{}:{}".format(
			str(self.Width),
			str(self.Height),
			gameID
		)

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
