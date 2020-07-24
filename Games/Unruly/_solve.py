import re, random

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
		columns = tuple([board[y][x] for y in range(self.Height)] for x in range(self.Width))

		for y in range(self.Height):
			# Check more block than 2 in line
			for x in range(self.Width-2):
				if self._map[y][x].Type == self._map[y][x+1].Type and self._map[y][x].Type == self._map[y][x+2].Type and self._map[y][x].Type != Block.EMPTY:
					return False
			# Check block counts in row
			if (board[y].count(1) > self.UniqueInX or
				board[y].count(0) > self.UniqueInX):
				return False

		for x in range(self.Width):
			# Check more block than 2 in line
			for y in range(self.Height-2):
				if self._map[y][x].Type == self._map[y+1][x].Type and self._map[y][x].Type == self._map[y+2][x].Type and self._map[y][x].Type != Block.EMPTY:
					return False
			# Check block counts in column
			if (columns[x].count(1) > self.UniqueInY or
				columns[x].count(0) > self.UniqueInY):
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

	@property
	def _invertedMap(self) -> list:
		"""
		Method create copy of map (blocks aren't copied) in other direction.
		Returns:
			list: 2D matrix with inverted map.
		"""
		return [[self._map[y][x] for y in range(self.Height)] for x in range(self.Width)]

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

	Attributes:
		Board (Board): Board object with map to solve.
	"""
	def __init__(self, board: Board) -> None:
		"""
		Constructor for 'Solve' class.

		Parameters:
			board (Board): Board object what shoud be solved.
		"""
		self.Board = board

	def solve(self) -> list:
		"""
		Method solve board and create binary matrix representing color of every block.

		Returns:
			list: 2D matrix with ints representing blocks color: 0 - White, 1 - Black.
		"""
		board = self.solveBoard()
		output = board.exportToBinaryMatrix()
		if None in sum(output, []):
			print("Sorry, I cannot solve this Board.")
		return output

	def solveBoard(self) -> 'Board':
		"""
		Method solve Board.

		Returns:
			Board: Solved Board object.
		"""
		changes = 1
		usedLimits = set()
		while changes > 0:
			changes = 0

			addWalls = self.addWallsForDublesInLine()
			self.appendBlocks(addWalls)
			changes += len(addWalls)

			checkEmpty = self.checkEmptyBlockBetweenTwoInLine()
			self.appendBlocks(checkEmpty)
			changes += len(checkEmpty)

			checkOutOfBlocks = self.checkOutOfBlockOneColorInLine()
			self.appendBlocks(checkOutOfBlocks)
			changes += len(checkOutOfBlocks)

			limits = tuple(self.checkSessionLimits())
			if hash(limits) not in usedLimits:
				usedLimits.add(hash(limits))
				self.appendBlocks(limits)
				changes += len(limits)

		if None in sum(self.Board.exportToBinaryMatrix(), []):
			return self.randomizeOneBlock()
		else:
			return self.Board

	def appendBlocks(self, blockList: list) -> None:
		"""
		Method change blocks types by recived data.
		Parameters:
			blockList (list): List with connection points and block type: 0-White 1-Black. sch. [(<x>, <y>, <color>), ...]
		"""
		for block in blockList:
			self.Board[block[0], block[1]].Type = Block.WHITE if block[2] == 0 else Block.BLACK

	def addWallsForDublesInLine(self) -> list:
		"""
		Method search dubled blocks in one color and check existing his ways.

		Returns:
			list: List of coordinates where shoud be seted blocks and them color eg. [(3,5,0),(5,6,1)]
		"""
		output = []

		# For rows
		for row in self.Board._map:
			lastType = Block.EMPTY
			for x in range(self.Board.Width):
				if row[x].Type == lastType and lastType is not Block.EMPTY:
					if len(row) > x+1 and row[x+1].Type == Block.EMPTY:
						output.append((
							row[x].x+1,
							row[x].y,
							1 if lastType == Block.WHITE else 0
						))
					if x > 1 and row[x-2].Type == Block.EMPTY:
						output.append((
							row[x].x-2,
							row[x].y,
							1 if lastType == Block.WHITE else 0
						))
				else:
					lastType = row[x].Type

		#For columns
		for column in self.Board._invertedMap:
			lastType = Block.EMPTY
			for y in range(self.Board.Height):
				if column[y].Type == lastType and lastType is not Block.EMPTY:
					if len(column) > y+1 and column[y+1].Type == Block.EMPTY:
						output.append((
							column[y].x,
							column[y].y+1,
							1 if lastType == Block.WHITE else 0
						))
					if y > 1 and column[y-2].Type == Block.EMPTY:
						output.append((
							column[y].x,
							column[y].y-2,
							1 if lastType == Block.WHITE else 0
						))
				else:
					lastType = column[y].Type

		return output

	def checkOutOfBlockOneColorInLine(self) -> list:
		"""
		Method count blocks in line and check limits. If count of blocks are end, then other empty blocks fill with second color.

		Returns:
			list: List of coordinates where shoud be seted blocks and them color eg. [(3,5,0),(5,6,1)]
		"""
		output = []
		rows = self.Board.exportToBinaryMatrix()
		columns = [[rows[y][x] for y in range(len(rows))] for x in range(len(rows[0]))]

		#For rows
		for y in range(self.Board.Height):
			if None in rows[y]:
				block = None
				if rows[y].count(0) == self.Board.UniqueInX:
					block = 1
				elif rows[y].count(1) == self.Board.UniqueInX:
					block = 0
				if block is not None:
					for x in range(self.Board.Width):
						if rows[y][x] is None:
							output.append((
								x,
								y,
								block
							))

		#For columns
		for x in range(self.Board.Width):
			if None in columns[x]:
				block = None
				if columns[x].count(0) == self.Board.UniqueInY:
					block = 1
				elif columns[x].count(1) == self.Board.UniqueInY:
					block = 0
				if block is not None:
					for y in range(self.Board.Height):
						if columns[x][y] is None and (x, y, block) not in output:
							output.append((
								x,
								y,
								block
							))

		return output

	def checkEmptyBlockBetweenTwoInLine(self) -> list:
		"""
		Method search two blocks in line with this same color and one empty block between them.

		Returns:
			list: List of coordinates where shoud be seted blocks and them color eg. [(3,5,0),(5,6,1)]
		"""
		output = []

		#For row
		for row in self.Board._map:
			for x in range(self.Board.Width-2):
				if (row[x].Type == row[x+2].Type and
					row[x].Type is not Block.EMPTY and
					row[x+1].Type is Block.EMPTY):
					output.append((
						row[x+1].x,
						row[x+1].y,
						1 if row[x].Type == Block.WHITE else 0
					))

		#For column
		for column in self.Board._invertedMap:
			for y in range(self.Board.Height-2):
				if (column[y].Type == column[y+2].Type and
					column[y].Type is not Block.EMPTY and
					column[y+1].Type is Block.EMPTY):
					output.append((
						column[y+1].x,
						column[y+1].y,
						1 if column[y].Type == Block.WHITE else 0
					))

		return output

	def checkSessionLimits(self) -> list:
		output = []
		rows = [[self.Board._map[y][x].Type for x in range(self.Board.Width)] for y in range(self.Board.Height)]
		columns = [[rows[y][x] for y in range(self.Board.Height)] for x in range(self.Board.Width)]
		# Rows
		for y in range(self.Board.Height):
			countBlack, countWhite = rows[y].count(Block.BLACK), rows[y].count(Block.WHITE)
			minimumBlock = 0 if countWhite < countBlack else 1
			maxSessions = [[-1,0]]
			for x in range(self.Board.Width):
				if rows[y][x] in (Block.EMPTY, Block.WHITE if minimumBlock == 0 else Block.BLACK):
					if sum(maxSessions[-1]) == x:
						maxSessions[-1][1] += 1
					else:
						maxSessions.append([x, 1])
			maxSession = max(maxSessions, key=lambda x: x[1])
			exceptedMinimum = 3 * (self.Board.UniqueInX - (countWhite if minimumBlock == 1 else countBlack))
			if exceptedMinimum == 0:
				break
			xBlocks = []
			if maxSession[1] >= exceptedMinimum:
				xBlocks.extend(x for x in range(0, self.Board.Width) if rows[y][x] is Block.EMPTY and x not in range(maxSession[0], sum(maxSession)))
			if maxSession[1]-1 >= exceptedMinimum:
				xBlocks.extend((maxSession[0], sum(maxSession)-1))
			if maxSession[1]-2 == exceptedMinimum:
				xBlocks.extend((maxSession[0]+1, sum(maxSession)-2))
			for x in xBlocks:
				output.append((x, y, minimumBlock))

		# Columns
		for x in range(self.Board.Width):
			countBlack, countWhite = columns[x].count(Block.BLACK), columns[x].count(Block.WHITE)
			minimumBlock = 0 if countWhite < countBlack else 1
			maxSessions = [[-1,0]]
			for y in range(self.Board.Height):
				if rows[y][x] in (Block.EMPTY, Block.WHITE if minimumBlock == 0 else Block.BLACK):
					if sum(maxSessions[-1]) == y:
						maxSessions[-1][1] += 1
					else:
						maxSessions.append([y, 1])
			maxSession = max(maxSessions, key=lambda y: y[1])
			exceptedMinimum = 3 * (self.Board.UniqueInY - (countWhite if minimumBlock == 1 else countBlack))
			if exceptedMinimum == 0:
				break
			yBlocks = []
			if maxSession[1] >= exceptedMinimum:
				yBlocks.extend(y for y in range(0, self.Board.Width) if rows[y][x] is Block.EMPTY and y not in range(maxSession[0], sum(maxSession)))
			if maxSession[1]-1 >= exceptedMinimum:
				yBlocks.extend((maxSession[0], sum(maxSession)-1))
			if maxSession[1]-2 == exceptedMinimum:
				yBlocks.extend((maxSession[0]+1, sum(maxSession)-2))
			for y in yBlocks:
				output.append((x, y, minimumBlock))
		return list(set(output))

	def randomizeOneBlock(self) -> 'Board':
		"""
		Method clone Board and set random block with random color.

		Returns:
			Board: Board object with correct blocks.
		"""
		# To Do: Add better selecting block to random, not exactly random.
		allEmptyBlocks = sum(([(x,y) for x in range(self.Board.Width) if self.Board._map[y][x].Type is Block.EMPTY] for y in range(self.Board.Height)), [])
		randomedBlock = random.choice(allEmptyBlocks)
		for blockType in (Block.WHITE, Block.BLACK):
			board = self.Board.copy()
			board._map[randomedBlock[1]][randomedBlock[0]].Type = blockType
			if not board.isValid():
				continue
			solve = Solve(board)
			solvedBoard = solve.solveBoard()
			if solvedBoard.isValid() and None not in sum(solvedBoard.exportToBinaryMatrix(), []):
				return solvedBoard
		return self.Board
