from _solve import Board, Block, Solve
from _test_maps import *
import unittest, pdb



class Test_Board(unittest.TestCase):
	def Test_parsingBoardFromMatrix(self):
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

class Test_SolveMethods(unittest.TestCase):
	def getMapOfBlocksNotLinking(self, solution, ways: list = []):
		solver = Solve(Board.parse(TestLinks1))
		solver.Ways = ways

		linkingMap = solver.getMapOfBlocksNotLinking()
		for y in range(len(linkingMap)):
			for x in range(len(linkingMap[0])):
				self.assertEqual(
					linkingMap[y][x],
					solution[y][x],
					"Block on x:{} and y:{} is {}".format(
						x,
						y,
						"not linking" if solution[y][x] else "linking"
					)
				)

	def test_getMapOfBlocksNotLinking_noWays(self):
		self.getMapOfBlocksNotLinking(TestLinks1_NotLinking)

	def test_getMapOfBlocksNotLinking_withWays(self):
		ways = [
			[(2, 0), (2, 1), (1, 2)],
			[(2, 3), (3, 2)]
		]
		solution = [ list(x) for x in list(TestLinks1_NotLinking).copy() ]
		for x, y in ((2, 0), (2, 1), (2, 3)):
			solution[y][x] = False

		self.getMapOfBlocksNotLinking(solution, ways)

	def getMapOfBlocksNotLinked(self, solution, ways: list = []):
		solver = Solve(Board.parse(TestLinks1))
		solver.Ways = ways

		linkingMap = solver.getMapOfBlocksNotLinked()
		for y in range(len(linkingMap)):
			for x in range(len(linkingMap[0])):
				self.assertEqual(
					linkingMap[y][x],
					solution[y][x],
					"Block on x:{} and y:{} is {}".format(
						x,
						y,
						"not linked" if solution[y][x] else "linked"
					)
				)

	def test_getMapOfBlocksNotLinked_withWays(self):
		ways = [
			[(2, 0), (2, 1), (1, 2)],
			[(2, 3), (3, 2)]
		]
		solution = [ list(x) for x in list(TestLinks1_NotLinked).copy() ]
		for x, y in ((2, 1), (1, 2), (3, 2)):
			solution[y][x] = False
		self.getMapOfBlocksNotLinked(solution, ways)

	def test_getMapOfBlocksNotLinked_noWays(self):
		self.getMapOfBlocksNotLinked(TestLinks1_NotLinked)

	def test_getAllBlocksOnWay(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)

		dataSet = (
			({board[2, 1], board[2, 0]}, (2, 2), "TOP"),
			({board[2, 3]}, (2, 2), "BOTTOM"),
			({board[2, 1], board[3, 1]}, (1, 1), "RIGHT"),
			({board[0, 1]}, (1, 1), "LEFT"),
			({board[2, 2], board[3, 1]}, (1, 3), "TOP_RIGHT"),
			({board[1, 1], board[2, 2], board[3, 3]}, (0, 0), "BOTTOM_RIGHT"),
			({board[1, 2], board[0, 3]}, (2, 1), "BOTTOM_LEFT"),
			({board[1, 2], board[0, 1]}, (2, 3), "TOP_LEFT")
		)

		for data in dataSet:
			self.assertEqual(
				set(solver.getAllBlocksOnWay(
					getattr(Block, "DIRECTION_"+data[2]),
					data[1]
				)),
				data[0],
				"Test getAllBlocksOnWay with way: {} and starting point: x={}, y={}".format(
					" and ".join(x[0].upper()+x[1:].lower() for x in str(data[2]).split("_")),
					*data[1]
				)
			)

	def test_checkOnlyOneMove_noWays(self):
		board = Board.parse(TestLinks1)
		self.assertEqual(
			set(Solve(board).checkOnlyOneMove()),
			{
				(board[0,1], board[0,2]),
				(board[2,3], board[3,2]),
				(board[2,1], board[0,1]),
				(board[3,1], board[1,3]),
				(board[1,3], board[1,2]),
				(board[2,2], board[2,3]),
			}
		)

	def test_checkOnlyOneMove_withWays(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)
		solver.Ways = [
			[(2,1), (0,1), (0,2)],
			[(3,1), (1,3)]
		]
		self.assertEqual(
			set(solver.checkOnlyOneMove()),
			{
				(board[2,3], board[3,2]),
				(board[1,3], board[1,2]),
				(board[2,2], board[2,3]),
			}
		)

	def test_checkOnlyOneLinking_noWays(self):
		board = Board.parse(TestLinks1)
		self.assertEqual(
			set(Solve(board).checkOnlyOneLinking()),
			{
				(board[2,0], board[2,1]),
				(board[2,1], board[0,1]),
				(board[0,1], board[0,2]),
				(board[0,2], board[2,2]),
				(board[2,2], board[2,3]),
				(board[2,3], board[3,2]),
				(board[3,2], board[3,1]),
				(board[3,1], board[1,3]),
				(board[1,3], board[1,2]),
				(board[1,2], board[3,0]),
			}
		)

	def test_checkOnlyOneLinking_withWays(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)
		solver.Ways = [
			[(1,3), (1,2), (3,0)],
			[(2,2), (2,3)],
		]
		self.assertEqual(
			set(solver.checkOnlyOneLinking()),
			{
				(board[2,0], board[2,1]),
				(board[2,1], board[0,1]),
				(board[0,1], board[0,2]),
				(board[0,2], board[2,2]),
				(board[2,3], board[3,2]),
				(board[3,2], board[3,1]),
				(board[3,1], board[1,3]),
			}
		)





if __name__ == "__main__":
	unittest.main()
