import math, json, pdb

class Board:
	def __init__(self, width: int = None, height: int = None) -> None:
		self._map = ()
		self.Width = 0 if type(width) != int else width
		self.Height = 0 if type(height) != int else height

	def getValuesMatrix(self):
		return tuple(
			tuple(block.Value for block in row)
			for row in self._map
		)

	@classmethod
	def _parseJSON(cls, data: str) -> 'Board':
		return cls._parseMatrix(json.loads(data))

	@classmethod
	def _parseMatrix(cls, matrix: tuple) -> 'Board':
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
	def parse(cls, data) -> 'Board':
		if type(data) == str:
			return cls._parseJSON(data)
		elif type(data) in (tuple, list):
			return cls._parseMatrix(data)

	def __getitem__(self, pos: tuple) -> tuple:
		return None if pos[0] >= self.Width or pos[1] >= self.Height else self._map[pos[1]][pos[0]]

	def __len__(self) -> tuple:
		return (self.Width, self.Height)

class Block:
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
	def __init__(self, board: Board) -> None:
		self.Board = board
		self.Ways = []

	def checkOnlyOneMove(self) -> list:
		unlinking = self.getMapOfBlocksNotLinking()
		unlinked = self.getMapOfBlocksNotLinked()
		output = []
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
									unlkd.append(self.Board[wx, wy])
						except IndexError:
							break
						else:
							step += 1
					if len(unlkd) == 1:
						inWays = False
						for way in self.Ways+output:
							if (unlkd[0].x, unlkd[0].y) in way:
								inWays = True
								break
						if not inWays:
							output.append((block, unlkd[0]))
							unlinked[unlkd[0].y][unlkd[0].x] = False
							unlinking[block.y][block.x] = False
		return output

	def checkOnlyOneLinking(self) -> list:
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

	def commitWay(self, way: list) -> None:
		firstElementValue = None
		for step in range(len(way)):
			firstElementValue = self.Board[way[step][0], way[step][1]].Value
			if firstElementValue is not None:
				firstElementValue -= step
				break
		if type(firstElementValue) is not int or firstElementValue < 1:
			raise ValueError("Cannot find any correct value in this Way!")
		for wayNum in range(len(way)):
			self.Board[way[wayNum][0], way[wayNum][1]].Value = firstElementValue+wayNum

	@staticmethod
	def _getWayCoordinatesIncrement(direction: int) -> tuple:
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
		blocks = [ [True]*self.Board.Width for _ in range(self.Board.Height) ]

		allBlocksInBoard = dict(self._allNumeredBlocksInBoard())
		for block in allBlocksInBoard.keys():
			if block + 1 in allBlocksInBoard.keys():
				axis = allBlocksInBoard[block]
				blocks[axis[1]][axis[0]] = False

		for x in range(self.Board.Width):
			for y in range(self.Board.Height):
				if self.Board[x, y].isEnd:
					blocks[y][x] = False

		for way in self.Ways:
			for block in way[0:-1]:
				blocks[block[1]][block[0]] = False

		return blocks

	def getMapOfBlocksNotLinked(self) -> list:
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
		allBlocksInBoard = []
		for x in range(self.Board.Width):
			for y in range(self.Board.Height):
				if self.Board[x, y].Value != None:
					allBlocksInBoard.append((self.Board[x, y].Value, (x, y)))
		return allBlocksInBoard
