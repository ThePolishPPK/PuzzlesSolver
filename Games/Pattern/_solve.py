import enum, re, copy

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

	def __repr__(self) -> str:
		return "<Block x={} y={} type={}>".format(
			self.x,
			self.y,
			"Black" if self.type is BlockType.BLACK else
				"White" if self.type is BlockType.WHITE else "Empty",
		)

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

	def getLineData(self) -> tuple:
		"""
		Method create data set with line and block sessions on those line.

		Returns:
			tuple: Tuple collection in schema: (((<Block>, ...), (<int>, ...)), ...)
		"""
		rows = [(self.rowMap[y], self.inRow[y]) for y in range(self.Height)]
		cols = [(self.columnMap[y], self.inColumn[y]) for y in range(self.Height)]
		return sum([rows, cols], [])

	def exportToBinary(self) -> str:
		"""
		Method save blocks to binary representation.

		Returns:
			str: String with binary.
		"""
		output  = ""
		for x in sum([list(x) for x in self._map], []):
			output += "1" if x.type is BlockType.BLACK else "0"
		return output

	def isValid(self) -> bool:
		"""
		Method check validity of board.

		Returns:
			bool: Validity status, True if valid else False
		"""
		for line, blocks in self.getLineData():
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

	def __str__(self) -> str:
		output = []
		for l in self._map:
			output.append(''.join([
				(
					"B " if x.type == BlockType.BLACK else
					"W " if x.type == BlockType.WHITE else
					"E "
				) for x in l
			]))
		return '\n'.join(output)

class Solve:
	"""
	Attributes:
		Board (Board): Board object what shoud be solved.
	"""
	def __init__(self, board: Board):
		assert type(board) is Board
		self.Board = board

	def searchHardBlocks(self):
		"""
		Method search blocks what is static without looking on block session offset (max and min).
		Returns:
			tuple: Collection with point and block to set. Schema: (((<x>, <y>), BlockType.BLACK), ...)
		"""
		output = []
		for line, blocks in self.Board.getLineData():
			mapLine = self._mapSessionOnLine(line)
			right = copy.copy(mapLine)
			left = copy.copy(mapLine)
			hardBlocks = dict()

			for x, block in enumerate(blocks):
				hardBlocks[x] = [0]*len(line)
				try:
					caseIndex, case = next(filter(lambda y: len(y[1]) >= block, enumerate(left)))
				except:
					pass
				else:
					for bl in case[0:block]:
						hardBlocks[x][line.index(bl)] += 0.5
					left[caseIndex] = case[block+1:]

			for x, block in list(enumerate(blocks))[::-1]:
				try:
					caseIndex, case = list(filter(lambda y: len(y[1]) >= block, enumerate(right)))[-1]
				except:
					pass
				else:
					for bl in case[-block:]:
						hardBlocks[x][line.index(bl)] += 0.5
					right[caseIndex] = case[0:-block-1]
				for x in range(len(line)):
					if len(tuple(y[x] for y in hardBlocks.values() if y[x] >= 1.0)) > 0:
						if line[x].type is BlockType.EMPTY:
							output.append(((line[x].x, line[x].y), BlockType.BLACK))
				globalLine = [0]*len(line)
				for ln in hardBlocks.values():
					if len(list(filter(lambda x: x >= 1, ln))) > 0:
						for x in range(len(line)):
							globalLine[x] += ln[x]
					else:
						break
				else:
					for x in range(len(line)):
						if globalLine[x] == 0:
							if line[x].type is BlockType.EMPTY:
								output.append(((line[x].x, line[x].y), BlockType.WHITE))
		return tuple(set(output))

	def appendBlocks(self, blocks: tuple):
		"""
		Method append blocks to board.

		Parameters:
			blocks (tuple): Tuple with blocks data. Schema: (((<x>, <y>), <BlockType>), ...)
		"""
		assert type(blocks) == tuple
		for el in blocks:
			assert type(el[0]) == tuple and type(el[0][0]) == int and type(el[0][1]) == int
			assert type(el[1]) == BlockType

		for pos, blType in blocks:
			self.Board.rowMap[pos[1]][pos[0]].type = blType

	def searchCompletedLines(self) -> tuple:
		"""
		Method search lines were dependences are completed and collect other blocks in line to data set.

		Returns:
			tuple: Tuple with blocks data.
		"""
		output = []
		for line, blocks in self.Board.getLineData():
			lineTypes = tuple(map(lambda x: x.type, line))
			if BlockType.BLACK not in lineTypes:
				continue
			index = lineTypes.index(BlockType.BLACK)
			for blID, block in enumerate(blocks):
				if (lineTypes[index:index+block].count(BlockType.BLACK) == block
					and (index+block+1 >= len(line) or lineTypes[index+block] is not BlockType.BLACK)):
					try:
						index = lineTypes.index(BlockType.BLACK, index+block)
					except ValueError:
						if blID != len(blocks)-1:
							break
				else:
					break
			else:
				for bl in line:
					if bl.type == BlockType.EMPTY:
						output.append(((bl.x, bl.y), BlockType.WHITE))
		return tuple(set(output))

	@staticmethod
	def _mapSessionOnLine(line):
		mapLine = [[]]
		for element in line:
			if element.type in (BlockType.BLACK, BlockType.EMPTY):
				mapLine[-1].append(element)
			else:
				if len(mapLine[-1]) != 0:
					mapLine.append([])
		return mapLine

























