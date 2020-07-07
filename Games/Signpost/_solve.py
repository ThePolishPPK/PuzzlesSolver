import math, json, re, pdb

class Board:
	"""
	Class 'Board' it's a representation of board in game.
	
	Attributes:
		_map (tuple): Contain 'Block' objects in matrix (2D array) in schema like: ( (<Block object>, ...), (...), ... ).
		Width (int): Contain width of board.
		Height (int): Contain height of board.
	"""

	def __init__(self, width: int = None, height: int = None) -> None:
		"""
		Constructor for 'Board' class.
		
		Parameters:
			width (int): Width of board. (default: None)
			height (int): Height of board. (default: None)
		"""
		self._map = ()
		self.Width = 0 if type(width) != int else width
		self.Height = 0 if type(height) != int else height

	def getValuesMatrix(self):
		"""
		Mathod get values for every block and pack in to tuple 2D matrix.
		
		Returns:
			Tuple: 2D array of board values.
		"""
		return tuple(
			tuple(block.Value for block in row)
			for row in self._map
		)

	@classmethod
	def _parseJSON(cls, data: str) -> 'Board':
		"""
		Method parse json string and return 'Board' object.

		Parameters:
			data (str): JSON string with saved map.

		Returns:
			Board: Board object with map defined by JSON data.
		"""
		return cls._parseMatrix(json.loads(data))

	@classmethod
	def _parseMatrix(cls, matrix: tuple) -> 'Board':
		"""
		Method parse 2D tuple data set to Board.

		Parameters:
			matrix (tuple): Matrix with block data in schema: ( ( (<value>, <direction>), ...), ...)

		Returns:
			Board: Board object with map defined by gived matrix.
		"""
		# Matrix validation
		width = None
		for row in matrix:
			if width != None:
				assert len(row) == width
			else:
				width = len(row)

		board = cls(width, len(matrix))
		boardMap = []
		for row in range(len(matrix)):
			line = []
			for column in range(len(matrix[row])):
				line.append(
					Block(
						x=column,
						y=row,
						direction=matrix[row][column][1],
						value=matrix[row][column][0],
						isEnd=(matrix[row][column][0] == (width * len(matrix)))
					)
				)
			boardMap.append(tuple(line))
		board._map = tuple(boardMap)
		return board

	@classmethod
	def _parseGameID(cls, gameID: str) -> 'Board':
		"""
		Method parse Game ID to Board object.

		Parameters:
			gameID (str): String in schema(RegExp): "[0-9]+x[0-9]+:([0-9]*[a-h])+" eg. "2x2:1cfc4a"

		Returns:
			Board: Board object with map from gameID.
		"""
		boardMap = []
		width, height = (int(size) for size in gameID.split(":")[0].lower().split("x"))
		blocks = re.finditer("(?P<Value>([0-9]+)?)(?P<Direction>[a-h])", gameID.split(":")[-1])
		directions = {
			'a': Block.DIRECTION_TOP,
			'b': Block.DIRECTION_TOP_RIGHT,
			'c': Block.DIRECTION_RIGHT,
			'd': Block.DIRECTION_BOTTOM_RIGHT,
			'e': Block.DIRECTION_BOTTOM,
			'f': Block.DIRECTION_BOTTOM_LEFT,
			'g': Block.DIRECTION_LEFT,
			'h': Block.DIRECTION_TOP_LEFT
		}
		for y in range(height):
			line = []
			for x in range(width):
				block = next(blocks)
				line.append(Block(
					x,
					y,
					value=int(block.group("Value")) if block.group("Value") != "" else None,
					direction=directions[block.group("Direction").lower()]
				))
			boardMap.append(line)
		board = cls(width, height)
		board._map = boardMap
		return board

	@classmethod
	def parse(cls, data) -> 'Board':
		"""
		Method detect type of data and create map.
		Allowed types of data: tuple matrix, JSON matrix data, GameID string.

		Parameters:
			data: Mixed type, contain board map data.

		Returns:
			Board: Board object with map maked by given data.
		"""
		if type(data) == str:
			if re.search(r"^[0-9]+x[0-9]+:([0-9]*[a-h])+$", data) is not None:
				return cls._parseGameID(data)
			else:
				return cls._parseJSON(data)
		elif type(data) in (tuple, list):
			return cls._parseMatrix(data)

	def exportToJSON(self) -> str:
		"""
		Method convert board map to JSON data.

		Returns:
			str: Board map encoded in JSON data.
		"""
		return json.dumps(
			[
				[
					[x.Value, x.Direction]
					for x in y
				]
				for y in self._map
			]
		)

	def exportToGameID(self) -> str:
		"""
		Method convert board map to GameID data string.

		Returns:
			str: GameID string in fromat (RegExp): "[0-9]+x[0-9]+:([0-9]*[a-h])+"
		"""
		output = "%sx%s:"%(str(self.Width), str(self.Height))
		for y in range(self.Height):
			for x in range(self.Width):
				output += "" if self[x,y].Value is None else str(self[x,y].Value)
				output += chr(97 + (0 if self[x,y].Direction is None else self[x,y].Direction))
		return output

	def __getitem__(self, pos: tuple) -> tuple:
		return None if pos[0] >= self.Width or pos[1] >= self.Height else self._map[pos[1]][pos[0]]

	def __len__(self) -> tuple:
		return (self.Width, self.Height)

class Block:
	"""
	Class 'Block' this is representation for every block on Board.

	Attributes:
		x (int): Value location on x axis. (default: None)
		y (int): Value location on y axis. (default: None)
		Direction (int): Integer value for direction way, position 0 is for TOP and next position is in clockwise direction. (default: None)
		Value (int): Value of block Value. (default: None)
		isStart (bool): Inform about block status if that is first block (by number equal 1).
		isEnd (bool): Inform about block status if that is last block (by number width*height or gived information).
	"""
	# Direction in clockwise, starting from the top
	DIRECTION_TOP = 0
	DIRECTION_TOP_RIGHT = 1
	DIRECTION_RIGHT = 2
	DIRECTION_BOTTOM_RIGHT = 3
	DIRECTION_BOTTOM = 4
	DIRECTION_BOTTOM_LEFT = 5
	DIRECTION_LEFT = 6
	DIRECTION_TOP_LEFT = 7
	
	_isEnd = False
	
	def __init__(self, x: int, y: int, direction: int = None, value: int = None, isEnd: bool = False) -> None:
		"""
		Constructor for 'Block' class.

		Parameters:
			x (int): Location on x axis.
			y (int): Location on y axis.
			direction (int): Integer value for direction way, position 0 is for TOP and next position is in clockwise direction. (default: None)
			value (int): Value of block Value. (default: None)
			isEnd (bool): Define block status as last block. (default: False)
		"""
		self.x = x if type(x) == int else None
		self.y = y if type(y) == int else None
		self.Direction = None if type(direction) != int or direction >= 8 else direction
		self.Value = None if type(value) != int else value

		if isEnd == True:
			# Check Block value for probability of being end block.
			assert math.sqrt(value) % 1 == 0
			self._isEnd = True

	@property
	def isEnd(self) -> bool:
		return self._isEnd

	@property
	def isStart(self) -> bool:
		return (self.Value == 1) if self.Value != None else False

	def __repr__(self):
		return "<Block(x={}, y={}, direction={}, value={})>".format(
			self.x,
			self.y,
			self.Direction,
			self.Value
		)


class Solve:
	"""
	Class 'Solve' make all operations on board and blocks to solve.

	Schemats:
		ConnectionPoint: It's point described in tuple as (<x>, <y>).

	Attributes:
		Board (Board): Board object on witch operation will be performed.
		Ways (list): List of ways. Schema: [[<ConnectionPoint>, <ConnectionPoint>, ...], ...]
	"""
	def __init__(self, board: Board) -> None:
		"""
		Constructor for 'Solve' class

		Parameters:
			board (Board): Board object with defined map.
		"""
		self.Board = board
		self.Ways = []
		self.InvalidWays = set()

	def solve(self) -> list:
		"""
		Method execute all operations to solve game.

		Returns:
			tuple: 2D matrix of block Values from solved board.
		"""
		changes = 700
		while changes != 0:
			
			changes -= 1
			
			onlyOneLinking = self.checkOnlyOneLinking()
			self.addConnectionPointsToWays(onlyOneLinking)
			
			onlyOneMove = self.checkOnlyOneMove()
			self.addConnectionPointsToWays(onlyOneMove)
			
			onlyOneOnWay = self.checkOneBlockOnWay()
			self.addConnectionPointsToWays(onlyOneOnWay)
			
			for way in self.Ways:
				try:
					self.commitWay(way)
				except:
					pass
				else:
					self.Ways.remove(way)
		return self.Board.getValuesMatrix()

	def checkOnlyOneMove(self) -> list:
		"""
		Method check block to find all blocks that can remain linked.
		Method don't allow reps already existed connections in Ways or in Board.

		Returns:
			list: 2D list with connection points.
		"""
		unlinking = self.getMapOfBlocksNotLinking()
		unlinked = self.getMapOfBlocksNotLinked()
		output = []
		ol = None # Output Length
		while ol != len(output):
			ol = len(output)
			for x in range(self.Board.Width):
				for y in range(self.Board.Height):
					if unlinking[y][x]:
						block = self.Board[x, y]
						inc = self._getWayCoordinatesIncrement(block.Direction) # INCrementation
						
						unlkd = [] # UNLinKeD
						step = 1
						while True:
							wx, wy = (block.x+(inc[0]*step), block.y+(inc[1]*step))
							if wx < 0 or wy < 0:
								break
							try:
								if unlinked[wy][wx]:
									if block.Value is not None and self.Board[wx, wy].Value is not None:
										if block.Value + 1 == self.Board[wx, wy].Value:
											unlkd = [self.Board[wx, wy]]
									else:
										isInWay = False
										for way in self.Ways:
											if way[0] == (wx,wy) and way[-1] == (x,y):
												isInWay = True
										if not isInWay:
											unlkd.append(self.Board[wx, wy])
							except IndexError:
								break
							else:
								step += 1
						if len(unlkd) == 1:
							inWays = False
							for way in self.Ways+output:
								if (unlkd[0].x, unlkd[0].y) in way[1:]:
									inWays = True
									break
							output.append((block, unlkd[0]))
							unlinked[unlkd[0].y][unlkd[0].x] = False
							unlinking[block.y][block.x] = False
		return output

	def checkOnlyOneLinking(self) -> list:
		"""
		Method check blocks to find only one block linking block.
		Method don't allow reps of connections.

		Returns:
			list: 2D list with connection Points.
		"""
		unLinking = self.getMapOfBlocksNotLinking()
		unLinked = self.getMapOfBlocksNotLinked()
		output = []
		ol = None # Output Length
		while ol != len(output):
			ol = len(output)
			for x in range(self.Board.Width):
				for y in range(self.Board.Height):
					if unLinked[y][x]:
						block = self.Board[x, y]
						unlking = [] # UNLinKING
						for direction in range(8):
							inc = self._getWayCoordinatesIncrement(direction)
							step = 1
							while True:
								if type(unlking) == Block:
									break
								wx, wy = (x+(step*inc[0]), y+(step*inc[1]))
								if wx < 0 or wy < 0:
									break
								try:
									if unLinking[wy][wx]:
										b = self.Board[wx, wy]
										
										if self._getWayCoordinatesIncrement(b.Direction) == (-inc[0], -inc[1]):
											if block.Value is not None and b.Value is not None:
												if block.Value-1 == b.Value:
													unlking = b
											else:
												unlking.append(b)
								except IndexError:
									break
								else:
									step += 1
						if type(unlking) == Block:
							unlking = [unlking]
						if len(unlking) == 1:
							output.append((unlking[0], block))
							unLinking[unlking[0].y][unlking[0].x] = False
							unLinked[block.y][block.x] = False
		return output

	def checkOneBlockOnWay(self) -> list:
		"""
		Method checks block with values and posiblity of existing one block connection those points.
		Method don't allow reps in Ways.

		Returns:
			list: 2D list with connection points.
		"""
		data = []
		numeredBlocks = dict( (block[0], self.Board[block[1][0], block[1][1]]) for block in self._allNumeredBlocksInBoard() )
		num = 0
		for block in numeredBlocks.values():
			if (block.Value+2 in numeredBlocks.keys()
				and block.Value+1 not in numeredBlocks.keys()):
				for bl in self.getAllBlocksOnWay(block.Direction, (block.x, block.y)):
					if numeredBlocks[block.Value+2] in self.getAllBlocksOnWay(bl.Direction, (bl.x, bl.y)):
						data.append((block, bl))

		output = []
		for block in list(set(x[0] for x in data)):
			count = 0
			secondBlock = None
			for b in data:
				if b[0] == block:
					secondBlock = b[1]
					count += 1
			if count == 1:
				if secondBlock.Value is None:
					output.append((block, secondBlock))
					output.append((secondBlock, numeredBlocks[block.Value+2]))
		return output

	def commitWay(self, way: list) -> None:
		"""
		Method insert way connection points to Board map.
		When way is incorrect than method raise exception.

		Parameters:
			way (list): 2D list of connection points.
		"""
		firstElementValue = None
		for step in range(len(way)):
			firstElementValue = self.Board[way[step][0], way[step][1]].Value
			if firstElementValue is not None:
				firstElementValue -= step
				break
		if type(firstElementValue) is not int or firstElementValue < 1:
			if way in self.Ways:
				self.Ways.remove(way)
			raise ValueError("Cannot find any correct value in this Way!")
		nums = self._allNumeredBlocksInBoard()
		for wayNum in range(len(way)):
			for numeredBlock in nums:
				if (firstElementValue+wayNum == numeredBlock[0]
					and tuple(numeredBlock[1]) != tuple(way[wayNum][0:2])):
					raise ValueError("Cannot repeat value!")
				
			if (self.Board[way[wayNum][0], way[wayNum][1]].Value is not None
				and self.Board[way[wayNum][0], way[wayNum][1]].Value != firstElementValue+wayNum):
				if way in self.Ways:
					self.Ways.remove(way)
				self.InvalidWays.add(set(way))
				raise ValueError("Invalid way")

		for wayNum in range(len(way)):
			self.Board[way[wayNum][0], way[wayNum][1]].Value = firstElementValue+wayNum

	def addConnectionPointsToWays(self, connectionPoints: list) -> None:
		"""
		Method add connection points to Ways.

		Schemats:
			ConnectionPoint: It's point described in tuple as (<x>, <y>).

		Parameters:
			connectionPoints (list): List of connections. Schema: [[<ConnectionPoint>, <ConnectionPoint>], ...]
		"""
		self.Ways.extend([[(conn[0].x, conn[0].y), (conn[1].x, conn[1].y)] for conn in connectionPoints])
		self.compressWays()

	def compressWays(self) -> None:
		"""
		Method search connections between ways and connect them.
		"""
		changes = 1
		while changes > 0:
			changes = 0
			way = 0
			while way < len(self.Ways):
				step = 0
				while step < len(self.Ways):
					if way >= len(self.Ways):
						break
					delete = False
					if self.Ways[step][0] == self.Ways[way][-1]:
						self.Ways[way] += self.Ways[step][1:]
						changes += 1
						delete = True
					if self.Ways[step][-1] == self.Ways[way][0]:
						self.Ways[way] = self.Ways[step] + self.Ways[way][1:]
						changes += 1
						delete = True
					if delete:
						del self.Ways[step]
					step += 1
				way += 1

	@staticmethod
	def _getWayCoordinatesIncrement(direction: int) -> tuple:
		"""
		Method return incrementation ways. Method describe what axis is growing, what is decreases and what is not changed.

		Parameters:
			direction (int): Integer value for direction.

		Returns:
			tuple: Incrementation ways in schema: (<x>, <y>).
		"""
		if direction == Block.DIRECTION_TOP:
			x, y = 0, -1
		elif direction == Block.DIRECTION_TOP_LEFT:
			x, y = -1, -1
		elif direction == Block.DIRECTION_LEFT:
			x, y = -1, 0
		elif direction == Block.DIRECTION_BOTTOM_LEFT:
			x, y = -1, 1
		elif direction == Block.DIRECTION_BOTTOM:
			x, y = 0, 1
		elif direction == Block.DIRECTION_BOTTOM_RIGHT:
			x, y = 1, 1
		elif direction == Block.DIRECTION_RIGHT:
			x, y = 1, 0
		elif direction == Block.DIRECTION_TOP_RIGHT:
			x, y = 1, -1
		else:
			raise ValueError("Parameter 'direction' isn't correct")
		return (x, y)

	def getAllBlocksOnWay(self, direction: int, startPoint: tuple) -> list:
		"""
		Method collect all blocks on way other block by location and direction.

		Parameters:
			direction (int): Integer value of direction.
			startPoint (tuple): Coordinates of start point (not included in result).

		Returns:
			list: List of 'Block' objects.
		"""
		x, y = self._getWayCoordinatesIncrement(direction)

		step = 1
		blocks = []
		while True:
			wx, wy = (startPoint[0] + (step*x), startPoint[1] + (step*y))
			if wx not in range(self.Board.Width) or wy not in range(self.Board.Height):
				break
			blocks.append(self.Board[wx, wy])
			step += 1
		return blocks

	def getMapOfBlocksNotLinking(self) -> list:
		"""
		Method search all blocks that aren't linking and create matrix map with describing it.

		Returns:
			list: 2D matrix with bool values, what block are not linking (True) and what is (False).
		"""
		blocks = [ [True]*self.Board.Width for _ in range(self.Board.Height) ]

		allBlocksInBoard = dict(self._allNumeredBlocksInBoard())

		for x in range(self.Board.Width):
			for y in range(self.Board.Height):
				if self.Board[x, y].Value is not None:
					if self.Board[x, y].Value+1 in allBlocksInBoard.keys():
						blocks[y][x] = False
				if self.Board[x, y].isEnd:
					blocks[y][x] = False

		for way in self.Ways:
			for block in way[0:-1]:
				blocks[block[1]][block[0]] = False

		return blocks

	def getMapOfBlocksNotLinked(self) -> list:
		"""
		Method search block that are not linked, and create matrix map when decribe it.

		Returns:
			list: 2D matrix taht contain bool values, if block is linked (False) and not linked (True).
		"""
		blocks = [ [True]*self.Board.Width for _ in range(self.Board.Height) ]

		allUsedBlocksInBoard = dict(self._allNumeredBlocksInBoard())
		for block in allUsedBlocksInBoard.keys():
			if block-1 in allUsedBlocksInBoard.keys():
				blocks[allUsedBlocksInBoard[block][1]][allUsedBlocksInBoard[block][0]] = False

		for x in range(self.Board.Width):
			for y in range(self.Board.Height):
				if self.Board[x, y].isStart:
					blocks[y][x] = False

		for way in self.Ways:
			for block in way[1:]:
				blocks[block[1]][block[0]] = False

		return blocks

	def _allNumeredBlocksInBoard(self) -> list:
		"""
		Method collect all block from Board map that value are not equal None.

		Returns:
			list: List with Block objects.
		"""
		allBlocksInBoard = []
		for x in range(self.Board.Width):
			for y in range(self.Board.Height):
				if self.Board[x, y].Value != None:
					allBlocksInBoard.append((self.Board[x, y].Value, (x, y)))
		return allBlocksInBoard
