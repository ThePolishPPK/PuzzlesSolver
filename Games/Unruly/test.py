import unittest, pudb
from _solve import Board, Block, Solve

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


class Test_Solve(unittest.TestCase):
	def test_addWallsForDublesInLine(self):
		self.assertEqual(
			sorted(tuple(Solve(Board.parse("8x8:ECCCBdccbdgcFbcDEc")).addWallsForDublesInLine())),
			sorted((
				(3, 1, 1),
				(3, 4, 1),
				(1, 4, 1),
				(1, 7, 1),
				(7, 2, 0)
			))
		)
		self.assertEqual(
			sorted(tuple(Solve(Board.parse("14x14:EbCejbhdKAHaMcCDbFgFgcBgbAcKaCdbeAGBAGAJCgab")).addWallsForDublesInLine())),
			sorted((
				(2, 3, 0),
				(2, 6, 0),
				(0, 9, 1),
				(0, 12, 1),
				(4, 11, 0),
				(3, 12, 0),
				(6, 12, 0),
				(6, 3, 0),
				(9, 3, 0),
				(10, 0, 1),
				(10, 3, 1),
				(9, 11, 0),
				(12, 11, 0),
				(12, 6, 1),
				(12, 9, 1),
				(13, 7, 0),
				(13, 10, 0),
				(10, 13, 1),
				(13, 13, 1)
			))
		)

	def test_checkEmptyBlockBetweenTwoInLine(self):
		self.assertEqual(
			sorted(tuple(Solve(Board.parse("10x10:aaDGbEAfCAaNabbbbCbBbbCoBBFcca")).checkEmptyBlockBetweenTwoInLine())),
			sorted((
				(1, 5, 1),
				(3, 5, 1),
				(4, 6, 1),
				(3, 7, 1),
				(7, 4, 1),
				(6, 3, 1),
				(6, 8, 0)
			))
		)
		self.assertEqual(
			sorted(tuple(Solve(Board.parse("10x10:bAdbJBlcaCACGbfGAdlCBedac")).checkEmptyBlockBetweenTwoInLine())),
			sorted((
				(0, 3, 0),
				(2, 4, 1),
				(7, 0, 1),
				(6, 8, 0),
				(5, 7, 0)
			))
		)

	def test_checkOutOfBlockOneColorInLine(self):
		self.assertEqual(
			sorted(tuple(Solve(Board.parse("8x8:EcbCeabaAEFABBcbAaAaIaEb")).checkOutOfBlockOneColorInLine())),
			sorted((
				(1, 0, 1),
				(1, 3, 1),
				(1, 6, 1),
				(0, 2, 1),
				(3, 2, 1),
				(7, 2, 1),
				(4, 3, 0),
				(4, 6, 0),
				(4, 7, 0),
				(6, 0, 0),
				(6, 1, 0),
				(6, 3, 0),
				(6, 6, 0),
				(0, 4, 0),
				(3, 4, 0),
				(5, 4, 0),
				(7, 4, 0),
				(0, 5, 1),
				(2, 5, 1),
			))
		)

	def test_solve(self):
		dataSet = (
			("8x8:ABlBBgCCjDfahd", "1010110001011001101001101001100101010011101011000110011001010011"),
			("14x14:AciBEgDbebbecHJAdcIdaBCAliBACpcCADbacgCcbmcCcCa", "1100101001100111001100110100001101011010101101001001100101101100100110100100110100111001001100110101101100100110001100110110101100101010010100101101011001101100100101100100110110101000110101100101"),
		)
		for data in dataSet:
			self.assertEqual(
				"".join((str(x) for x in sum(Solve(Board.parse(data[0])).solve(), []))),
				data[1]
			)







if __name__ == "__main__":
	unittest.main()
