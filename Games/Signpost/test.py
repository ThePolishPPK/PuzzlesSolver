from _solve import Board, Block, Solve
from _test_maps import *
import unittest, pdb



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
				(board[2,0], board[2,1]),
				(board[0,2], board[2,2]),
				(board[3,2], board[3,1]),
				(board[1,2], board[3,0])
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
				(board[2,0], board[2,1]),
				(board[0,2], board[2,2]),
				(board[3,2], board[3,1]),
				(board[1,2], board[3,0])
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

	def test_commitWay(self):
		board = Board.parse(TestLinks1)
		solver = Solve(Board.parse(TestLinks1))
		solver.Ways = [
			[(2,0), (2,1), (0,1)],
			[(2,3), (3,2), (3,1)],
		]
		solver.commitWay(solver.Ways[0])
		solver.commitWay(solver.Ways[1])
		board._map[1][2].Value = 5
		board._map[3][2].Value = 9
		board._map[2][3].Value = 10

		self.assertEqual(
			solver.Board.getValuesMatrix(),
			board.getValuesMatrix()
		)

	def test_addConnectionPointsToWays_noWays(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)
		points = [ # No logic connection, it's only ways
			(board[1,2], board[2,3]),
			(board[0,1], board[3,1]),
			(board[3,1], board[1,2])
		]
		solver.addConnectionPointsToWays(points)
		self.assertEqual(
			solver.Ways,
			[
				[(0,1), (3,1), (1,2), (2,3)]
			]
		)

	def test_addConnectionPointsToWays_withWays(self):
		board = Board.parse(TestLinks1)
		solver = Solve(board)
		points = [
			(board[1,2], board[1,1]),
			(board[0,1], board[2,2]),
			(board[3,3], board[2,0]),
		]
		solver.Ways = [
			[(1,3), (2,3), (1,0), (0,1)],
			[(3,0), (3,1), (3,2), (3,3)]
		]
		solver.addConnectionPointsToWays(points)
		self.assertEqual(
			solver.Ways,
			[
				[(1,3), (2,3), (1,0), (0,1), (2,2)],
				[(3,0), (3,1), (3,2), (3,3), (2,0)],
				[(1,2), (1,1)]
			]
		)

	def test_checkOneBlockOnWay(self):
		board = Board.parse("5x5:1hda12ea14abegaac20a6daa4aafaaaac16a")
		self.assertEqual(
			set(Solve(board).checkOneBlockOnWay()),
			{
				(board[3,0], board[3,1]),
				(board[3,1], board[0,1]),
			}
		)

	def test_solve(self):
		dataSet = [
			# ( MAP, SOLUTION )
			(Board1_4x4, Solution1_4x4),
			(Board2_4x4, Solution2_4x4),
			(
				"5x5:ed18dcfdaeceach1g25acfaag8aa22gbg",
				Board.parse("5x5:3e15d18d11c12f4d14a16e19c20e2a24c13h1g25a9c7f17a10a6g8a23a22g5b21g").getValuesMatrix()
			),
			(
				"7x7:1dfcdfegd26efg30dfedfbdbf45edad2gfaae38baaaha18bcd5hghebca33g12ag49a",
				Board.parse("7x7:1d8f15c43d16f19e14g9d26e35f25g30d21f47e6d36f24b39d13b31f45e37d7a3d2g41f20a44a17e38b23a42a29a40h46a18b27c32d5h4g28h48e22b11c34a33g12a10g49a").getValuesMatrix()
			),
			(
				"7x7:1d26cege27egda15eecgge46cddd22h11eaebecbhcdbba5eg37c39agd20hdga41ca42ghh49a",
				Board.parse("7x7:1d26c14e13g19e27e18g45d25a15e29e23c28g24g33e46c47d8d3d22h11e44a40e7b30e9c10b12h34c35d17b21b2a5e4g37c39a36g31d20h48d38g43a41c16a42g32h6h49a").getValuesMatrix()
			),
			(
				"7x7:1cd40dced35gda7eh14ggg47ecdadcgcbafehhdhgdge41gda18b21eaggcabb20ha49a",
				Board.parse("7x7:1c16d40d34c36e2d35g5d15a7e39h14g4g3g47e32c29d33a37d45c46g43c28b6a30f19e38h44h9d42h8g12d11g23e41g26d31a18b21e13a25g17g48c27a10b22b20h24a49a").getValuesMatrix()
			),
			(
				"12x12:51ddfeccdc108egf1fee85e132d117dagc144a7d95ef126ea14c81d110a18g59ed113g16efg50adc122cgg118e71e77gff44fc88c99cgf47c119fdh87gaf30c31cca42h120ad124h104afh32f93c21eh39dbb52fchh92gf127cca11g128ed140dd83hf56bg61bbchg40hgcb82hf142fc70bgcfah37eh134h96g54aa22a9daac4ghah74ggahbac35aa72c143aaag",
				Board.parse("12x12:51d84d125f131e111c107c112d25c108e24g26f1f66e20e85e132d117d106a116g62c144a7d95e63f126e19a14c81d110a18g59e114d113g16e8f15g50a79d43c122c78g121g118e71e77g123f90f44f102c88c99c98g100f47c119f103d105h87g89a48f30c31c41c80a42h120a2d124h104a45f115h32f93c21e101h39d6b94b52f91c109h17h92g57f127c12c13a11g128e36d140d135d83h34f56b55g61b23b27c29h28g40h60g141c33b82h133f142f68c70b69g53c129f46a49h37e97h134h96g54a65a22a9d130a5a75c4g38h76a139h74g3g67a64h86b10a137c35a58a72c143a138a73a136g").getValuesMatrix()
			),
			(Board3_16x16, Solution3_16x16),
			(BoardI, SolutionI)
		]
		for data in dataSet:
			solution = Solve(Board.parse(data[0])).solve()
			for y in range(len(data[1])):
				for x in range(len(data[1][y])):
					self.assertEqual(
						solution[y][x],
						data[1][y][x]
					)

if __name__ == "__main__":
	unittest.main()
