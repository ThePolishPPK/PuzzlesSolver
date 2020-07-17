import unittest
from _solve import Board, Block

class Test_Board(unittest.TestCase):
	def test_parseGameID(self):
		output = Board._parseGameID("6x6:aDdajdBBbcd")
		black = [(4,0), (1,4), (3,4)]
		white = [(0,0), (2,1), (3,1), (1,3), (5,3), (5,4), (2,5)]
		for x,y in ((x,y) for x in range(6) for y in range(6)):
			blockType = "Black" if (x,y) in black else "White" if (x,y) in white else "Empty"
			self.assertEqual(
				(output._map[y][x].x, output._map[y][x].y),
				(x, y),
				"Block has incorrect coordinates. Expected x={} and y={}, got x={} and y={}".format(
					x,
					y,
					output._map[y][x].x,
					output._map[y][x].y
				)
			)
			self.assertEqual(
				output._map[y][x].Type,
				getattr(Block, blockType.upper()),
				"Block with x={} and y={} shoud have Type={}".format(
					x,
					y,
					blockType
				)
			)

	def test_exportToGameID(self):
		board = Board(6, 6)
		board._map = [
			[Block(0,0,Block.EMPTY),Block(1,0,Block.EMPTY),Block(2,0,Block.EMPTY),Block(3,0,Block.WHITE),Block(4,0,Block.WHITE),Block(5,0,Block.EMPTY)],
			[Block(0,1,Block.EMPTY),Block(1,1,Block.EMPTY),Block(2,1,Block.EMPTY),Block(3,1,Block.WHITE),Block(4,1,Block.EMPTY),Block(5,1,Block.EMPTY)],
			[Block(0,2,Block.BLACK),Block(1,2,Block.EMPTY),Block(2,2,Block.EMPTY),Block(3,2,Block.EMPTY),Block(4,2,Block.EMPTY),Block(5,2,Block.BLACK)],
			[Block(0,3,Block.EMPTY),Block(1,3,Block.EMPTY),Block(2,3,Block.EMPTY),Block(3,3,Block.EMPTY),Block(4,3,Block.BLACK),Block(5,3,Block.EMPTY)],
			[Block(0,4,Block.BLACK),Block(1,4,Block.BLACK),Block(2,4,Block.EMPTY),Block(3,4,Block.EMPTY),Block(4,4,Block.EMPTY),Block(5,4,Block.EMPTY)],
			[Block(0,5,Block.EMPTY),Block(1,5,Block.BLACK),Block(2,5,Block.EMPTY),Block(3,5,Block.EMPTY),Block(4,5,Block.EMPTY),Block(5,5,Block.EMPTY)],
		]
		self.assertEqual(
			board.exportToGameID(),
			"6x6:daeCEEBAFe"
		)
















if __name__ == "__main__":
	unittest.main()
