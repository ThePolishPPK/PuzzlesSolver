import enum

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
	def _init_(self, x: int, y: int, blockType: BlockType):
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
		self._map = tuple( tuple(Block(x, y, BlockType.EMPTY
				for x in range(self.Width)
			) for y in range(self.Height) )