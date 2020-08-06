import enum, re

class BlockType(enum.Enum):
	"""
	Enumerate class inholding block types: EMPTY, BLACK, WHITE
	"""
	EMPTY = 0
	BLACK = 1
	WHITE = 2

class Block:
	"""
	Class contain information about every block like x position, y position and type.

	Attributes:
		x (int): X position on x axis.
		y (int): Y position on y axis.
		type (BlockType): Type of block.
	"""
	def __init__(self, x: int, y: int, blockType: BlockType):
		"""
		Constructor for Block class.

		Parameters:
			x (int): X position on x axis.
			y (int): Y position on y axis.
			blockType (BlockType): Type of block.
		"""
		assert type(x) == int
		assert type(y) == int 
		assert type(blockType) == BlockType
		self.x = x
		self.y = y
		self.type = blockType

class Board:
	"""
	Class represent board with blocks.

	Attributes:
		Width (int): Count of columns.
		Height (int): Count of rows.
		_map (tuple): Default map of blocks. Schema: ((<Block>, ...), ...)
		columnMap (tuple): Map schema based on columns. eg. Map[<column>][<row>]
		rowMap (tuple): Map schema based on rows. eg. Map[<row>][<column>]
		inRow (tuple): Session of black blocks in row. Schema: ((<int>, ...), ...)
		inColumn (tuple): Session of black blocks in column. Schema: ((<int>, ...), ...)
	"""

	_gameIDRegex = re.compile(
			r"^(?P<width>[0-9]+)x(?P<height>[0-9]+):(([0-9]+\.?)+(\/|$))+$"
		)

	def __init__(self, width: int, height: int):
		"""
		Constructor for Board class.

		Parameters:
			width (int): Board width.
			height (int): Board height.
		"""
		assert type(width) == int and width > 0
		assert type(height) == int and height > 0
		self.Width = width
		self.Height = height
		self._map = tuple( tuple(Block(x, y, BlockType.EMPTY)
				for x in range(self.Width)
			) for y in range(self.Height)
		)
		self.inRow = ( tuple() for _ in range(self.Height) )
		self.inColumn = ( tuple() for _ in range(self.Width) )

	@property
	def columnMap(self):
		return tuple( tuple( self._map[y][x]
				for y in range(self.Height)
			) for x in range(self.Width) )

	@property
	def rowMap(self):
		return self._map

	@classmethod
	def parseGameID(cls, gameID: str):
		"""
		Method parse game id to Board object.
		Parameters:
			gameID (str): GameID string. eg."3x3:1.1/1/1/1/1/2"
		"""
		assert type(gameID) == str and cls._gameIDRegex.search(gameID) is not None
		data = cls._gameIDRegex.search(gameID)
		width = int(data.group("width"))
		height = int(data.group("height"))
		assert width+height == gameID.count("/")+1
		board = cls(width, height)
		blockSessions = [
				tuple( int(y) for y in x.split(".") )
				for x in gameID.split(":")[1].split("/")
			]
		board.inRow = tuple(blockSessions[width:])
		board.inColumn = tuple(blockSessions[:width])
		return board

	def isValid(self) -> bool:
		"""
		Method check validity of board.

		Returns:
			bool: Validity status, True if valid else False
		"""
		rows = [(self.rowMap[y], self.inRow[y]) for y in range(self.Height)]
		cols = [(self.columnMap[y], self.inColumn[y]) for y in range(self.Height)]
		for line, blocks in sum([rows, cols], []):
			integerLine = list(map(lambda l: l.type.value, line))
			try:
				index = integerLine.index(BlockType.BLACK.value)
			except:
				if len(blocks) > 0:
					return False

			for blockSession in blocks:
				if index+blockSession < len(line) and line[index+blockSession] is BlockType.BLACK:
					return False
				if integerLine[index:index+blockSession].count(BlockType.BLACK.value) != blockSession:
					return False
				try:
					index = integerLine.index(BlockType.BLACK.value, index+blockSession)
				except:
					if blockSession is not blocks[-1]:
						return False
		return True





