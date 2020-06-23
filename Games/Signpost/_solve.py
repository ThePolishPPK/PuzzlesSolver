import math, json

class Board:
	def __init__(self, width: int = None, height: int = None) -> None:
		self._map = ()
		self.Width = 0 if type(width) != int else width
		self.Height = 0 if type(height) != int else height

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
		for row in matrix:
			line = []
			for block in row:
				line.append(
					Block(
						direction=block[1],
						value=block[0],
						isEnd=(block[0] == (width * len(matrix)))
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
		return None if pos[1] > self.Width or pos[0] > self.Height else self._map[pos[1]][pos[0]]

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
	
	def __init__(self, direction=None, value=None, isEnd=False) -> None:
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
