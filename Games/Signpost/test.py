from _solve import Board, Block
import unittest, pdb

Board1_4x4 = (
	( (1, Block.DIRECTION_BOTTOM_RIGHT), (None, Block.DIRECTION_BOTTOM), (None, Block.DIRECTION_BOTTOM_LEFT), (None, Block.DIRECTION_BOTTOM) ),
	( (None, Block.DIRECTION_BOTTOM_RIGHT), (None, Block.DIRECTION_LEFT), (None, Block.DIRECTION_TOP_RIGHT), (None, Block.DIRECTION_TOP_LEFT) ),
	( (None, Block.DIRECTION_BOTTOM), (None, Block.DIRECTION_TOP), (None, Block.DIRECTION_RIGHT), (None, Block.DIRECTION_TOP_LEFT) ),
	( (None, Block.DIRECTION_TOP_RIGHT), (None, Block.DIRECTION_TOP_RIGHT), (None, Block.DIRECTION_TOP), (16, None) )
)

Solution1_4x4 = (
	(1, 4, 7, 15),
	(12, 11, 14, 6),
	(8, 10, 2, 3),
	(9, 5, 13, 16)
)


class Test_Board(unittest.TestCase):
	def test_parsingBoardFromMatrix(self):
		board = Board._parseMatrix(Board1_4x4)

		for y in range(len(Board1_4x4)):
			for x in range(len(Board1_4x4[y])):
				block = board[x, y]
				self.assertEqual(
					block.Value,
					Board1_4x4[y][x][0],
					"Block with coordinates x: {}, y: {} should have value equal '{}' got '{}'".format(
						x,
						y,
						Board1_4x4[y][x][0],
						block.Value
					)
				)

				self.assertEqual(
					block.Direction,
					Board1_4x4[y][x][1],
					"Block with coordinates x: {}, y: {} should have direction equal '{}' got '{}'".format(
						x,
						y,
						Board1_4x4[y][x][1],
						block.Direction
					)
				)












if __name__ == "__main__":
	unittest.main()
