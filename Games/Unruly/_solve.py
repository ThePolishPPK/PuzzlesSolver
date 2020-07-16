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
		"""
		pass

	@classmethod
	def parse(cls, data: str) -> 'Board':
		"""
		Method detect type of data and create Board object if it's possible.

		Parameters:
			data (str): Board map data.

		Returns:
			Board: Board with map created by data parameter.
		"""
		pass

	@classmethod
	def _parseGameID(cls, gameID: str) -> 'Board':
		"""
		Method parse inputed gameID and create Board object with map defined by data.

		Parameters:
			gameID (str): Data about map saved in specifed (by author) GameID style.

		Returns:
			Board: Board object with map defined by gameID parameter.
		"""
		pass

	def exportToGameID(self) -> str:
		"""
		Method parse data to GameID string.

		Returns:
			str: GameID Data.
		"""
		pass

	def copy(self) -> 'Board':
		"""
		Method make copy of Board object.

		Returns:
			Board: Cloned Board object.
		"""
		pass

	def __getitem__(self, location: tuple) -> 'Block':
		pass

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
		pass

	def __repr__(self) -> str:
		pass
