import math, json, re, copy

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
				value = int(block.group("Value")) if block.group("Value") != "" else None
				line.append(Block(
					x,
					y,
					value=value,
					direction=directions[block.group("Direction").lower()],
					isEnd=(value == width*height)
				))
			boardMap.append(tuple(line))
		board = cls(width, height)
		board._map = tuple(boardMap)
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

	def isValid(self) -> bool:
		"""
		Method check every block and correct connections.

		Returns:
			bool: Status about board.
		"""
		blocksByValues = dict((b.Value, (b.x, b.y)) for b in sum(self._map, ()))
		try:
			for n in range(1,self.Width*self.Height):
				block = blocksByValues[n]
				next = blocksByValues[n+1]
				inc = Solve._getWayCoordinatesIncrement(self._map[block[1]][block[0]].Direction)
				if inc[0] == 0:
					if next[0]-block[0] != 0:
						return False
				else:
					if (block[0]-next[0])*inc[0] > 0:
						return False
				if inc[1] == 0:
					if next[1]-block[1] != 0:
						return False
				else:
					if (block[1]-next[1])*inc[1] > 0:
						return False
				if inc[0] != 0 and inc[1] != 0:
					if (block[1]-next[1])*inc[1] != (block[0]-next[0])*inc[0]:
						return False
		except KeyError:
			return False
		return True

	def copy(self) -> 'Board':
		"""
		Method create copy of self object.

		Returns:
			Board: Copy of Board object.
		"""
		return Board.parse(self.exportToGameID())

	def __getitem__(self, pos: tuple) -> tuple:
		return None if (pos[0] >= self.Width or pos[1] >= self.Height or
			pos[0] < 0 or pos[1] < 0) else self._map[pos[1]][pos[0]]

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
		self._isEnd = True if isEnd else False

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
		alreadyExisedChanges = set()
		changes = 0
		while changes != hash((self.Board._map, tuple(tuple(l) for l in self.Ways))):
			changes = hash((self.Board._map, tuple(tuple(l) for l in self.Ways)))
			if changes in alreadyExisedChanges:
				break
			else:
				alreadyExisedChanges.add(changes)
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
		if None in sum(self.Board.getValuesMatrix(), ()):
			self = self.randomSetOneConnection()
		return self

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
		for x, y in ((x, y) for x in range(self.Board.Width) for y in range(self.Board.Height)):
			if unlinking[y][x]:
				block = self.Board[x, y]
				blocksOnWay = set()
				coordInc = self._getWayCoordinatesIncrement(block.Direction)
				step = 1
				while True:
					blockOnWay = self.Board[x+(step*coordInc[0]), y+(step*coordInc[1])]
					if blockOnWay is None:
						break
					if unlinked[blockOnWay.y][blockOnWay.x]:
						if block.Value is not None and blockOnWay.Value is not None:
							if block.Value+1 != blockOnWay.Value:
								step += 1
								continue
						blocksOnWay.add(blockOnWay)
					step += 1
				if len(blocksOnWay) == 1:
					blockOnWay = blocksOnWay.pop()
					output.append([
						(block.x, block.y),
						(blockOnWay.x, blockOnWay.y)
					])
					unlinking[block.y][block.x] = False
					unlinked[blockOnWay.y][blockOnWay.x] = False
		return output

	def checkOnlyOneLinking(self) -> list:
		"""
		Method check blocks to find only one block linking block.
		Method don't allow reps of connections.

		Returns:
			list: 2D list with connection Points.
		"""
		unlinking = self.getMapOfBlocksNotLinking()
		unlinked = self.getMapOfBlocksNotLinked()
		output = []
		for x, y in ((x,y) for x in range(self.Board.Width) for y in range(self.Board.Height)):
			if unlinked[y][x]:
				linking = []
				block = self.Board[x, y]
				for direction in range(8):
					linkingBlocks = self.getAllBlocksOnWay(direction, (x, y))
					for linkingBlock in linkingBlocks:
						if not linkingBlock.isEnd and unlinking[linkingBlock.y][linkingBlock.x]:
							if block in self.getAllBlocksOnWay(linkingBlock.Direction, (linkingBlock.x, linkingBlock.y)):
								if block.Value is not None and linkingBlock.Value is not None:
									if block.Value - 1 != linkingBlock.Value:
										continue
								linking.append(linkingBlock)
				if len(linking) == 1:
					output.append([
						(linking[0].x, linking[0].y),
						(block.x, block.y)
					])
		return output

	def checkOneBlockOnWay(self) -> list:
		"""
		Method checks block with values and posiblity of existing one block connection those points.
		Method don't allow reps in Ways.

		Returns:
			list: 2D list with connection points.
		"""
		output = []
		unlinking = self.getMapOfBlocksNotLinking()
		unlinked = self.getMapOfBlocksNotLinked()
		numeredBlocks = self._allNumeredBlocksInBoard()
		blocksByNumber = dict((block.Value, block) for block in numeredBlocks)
		for block in numeredBlocks:
			if unlinking[block.y][block.x]:
				if block.Value + 2 in blocksByNumber.keys() and block.Value + 1 not in blocksByNumber.keys():
					block3 = blocksByNumber[block.Value + 2]
					if unlinked[block3.y][block3.x]:
						possibleBlocks2 = []
						for block2 in self.getAllBlocksOnWay(block.Direction, (block.x, block.y)):
							if unlinking[block2.y][block2.x] and unlinked[block2.y][block2.x]:
								if block3 in self.getAllBlocksOnWay(block2.Direction, (block2.x, block2.y)):
									possibleBlocks2.append(block2)
						if len(possibleBlocks2) == 1:
							block2 = possibleBlocks2[0]
							output.append([
								(block.x, block.y),
								(block2.x, block2.y)
							])
							output.append([
								(block2.x, block2.y),
								(block3.x, block3.y)
							])
		return output

	def randomSetOneConnection(self) -> list:
		"""
		Method create copy of self object and create random link.
		If board are solved with that and other random links return values matrix else None.

		Returns:
			list: 2D Values matrix.
		"""
		blockToRandom = {}
		unlinking = self.getMapOfBlocksNotLinking()
		unlinked = self.getMapOfBlocksNotLinked()

		#Search unlinking points and them possible blocks to connect
		for x, y in ((x,y) for x in range(self.Board.Width) for y in range(self.Board.Height)):
			if unlinking[y][x]:
				block = self.Board[x,y]
				blockToRandom[block] = []
				for blockToConnect in self.getAllBlocksOnWay(block.Direction, (x,y)):
					if unlinked[blockToConnect.y][blockToConnect.x]:
						blockToRandom[block].append(blockToConnect)
		if len(tuple(blockToRandom.items())) == 0:
			return self

		#Select block with the lowest count of connections
		block = tuple(blockToRandom.items())[0][0]
		for bl in blockToRandom.items():
			if len(blockToRandom[block]) > len(bl[1]) and len(bl[1]) > 1:
				block = bl[0]

		#Clone Solve object, insert link and solve
		randomed = []
		for connect in blockToRandom[block]:
			solver = Solve(self.Board.copy())
			solver.Ways = copy.deepcopy(self.Ways)
			solver.Ways.append([(block.x, block.y), (connect.x, connect.y)])
			randomed.append(solver.solve())
			if randomed[-1].Board.isValid():
				break
		for solv in randomed:
			if solv.Board.isValid():
				return solv
		return self

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
			raise ValueError("Cannot find any correct value in this Way!")
		nums = self._allNumeredBlocksInBoard()
		for wayNum in range(len(way)):
			for numeredBlock in nums:
				if (firstElementValue+wayNum == numeredBlock.Value
					and (numeredBlock.x,numeredBlock.y) != tuple(way[wayNum][0:2])):
					raise ValueError("Cannot repeat value!")
				
			if (self.Board[way[wayNum][0], way[wayNum][1]].Value is not None
				and self.Board[way[wayNum][0], way[wayNum][1]].Value != firstElementValue+wayNum):
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
		self.Ways.extend(connectionPoints)
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

		allBlocksInBoard = dict(((block.Value, (block.x, block.y)) for block in self._allNumeredBlocksInBoard()))
		linkingWays = sum([way[0:-1] for way in self.Ways], [])

		for x in range(self.Board.Width):
			for y in range(self.Board.Height):
				if self.Board[x, y].Value is not None:
					if self.Board[x, y].Value+1 in allBlocksInBoard.keys():
						blocks[y][x] = False
				if self.Board[x, y].isEnd:
					blocks[y][x] = False

		for block in linkingWays:
				blocks[block[1]][block[0]] = False

		return blocks

	def getMapOfBlocksNotLinked(self) -> list:
		"""
		Method search block that are not linked, and create matrix map when decribe it.

		Returns:
			list: 2D matrix taht contain bool values, if block is linked (False) and not linked (True).
		"""
		blocks = [ [True]*self.Board.Width for _ in range(self.Board.Height) ]

		allUsedBlocksInBoard = dict(((block.Value, (block.x, block.y)) for block in self._allNumeredBlocksInBoard()))
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
					allBlocksInBoard.append(self.Board[x, y])
		return allBlocksInBoard
