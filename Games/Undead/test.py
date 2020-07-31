import unittest, pudb
from _solve import Board, Solve, Block, Direction

class TestBoard(unittest.TestCase):
	def test_parseGameID(self):
		parsed = Board.parseGameID("4x4:3,4,2,LaLReLLaRaRa,2,3,0,0,3,3,1,1,1,1,0,2,0,2,3,0")
		self.assertEqual(
			tuple(tuple(row) for row in parsed._map),
			(
				(Block.MIRROR_LEFT.value, Block.EMPTY.value, Block.MIRROR_LEFT.value, Block.MIRROR_RIGHT.value),
				(Block.EMPTY.value, Block.EMPTY.value, Block.EMPTY.value, Block.EMPTY.value),
				(Block.EMPTY.value, Block.MIRROR_LEFT.value, Block.MIRROR_LEFT.value, Block.EMPTY.value),
				(Block.MIRROR_RIGHT.value, Block.EMPTY.value, Block.MIRROR_RIGHT.value, Block.EMPTY.value)
			)
		)
		self.assertEqual(
			parsed.SeenFromTop,
			(2, 3, 0, 0)
		)
		self.assertEqual(
			parsed.SeenFromRight,
			(3, 3, 1, 1)
		)
		self.assertEqual(
			parsed.SeenFromBottom,
			(2, 0, 1, 1)
		)
		self.assertEqual(
			parsed.SeenFromLeft,
			(0, 3, 2, 0)
		)
		self.assertEqual(
			parsed.Vampires,
			4
		)
		self.assertEqual(
			parsed.Ghosts,
			3
		)
		self.assertEqual(
			parsed.Zombies,
			2
		)
		self.assertEqual(
			parsed.Width,
			4
		)
		self.assertEqual(
			parsed.Height,
			4
		)

class TestSolve(unittest.TestCase):
	def test_getAllSeenBlocks(self):
		solve = Solve(Board.parseGameID("4x4:3,3,2,LbLLRbLaLcLL,3,1,2,0,0,2,2,3,0,1,3,1,1,0,0,0"))
		self.assertEqual(
			# From Left on column with ID 1
			solve.getAllSeenBlocks(Direction.LEFT, 1),
			((1,2,1),)
		)
		self.assertEqual(
			# From Left on column with ID 0
			solve.getAllSeenBlocks(Direction.LEFT, 0),
			((1,0,1),)
		)
		self.assertEqual(
			# From Bottom on column with ID 1
			solve.getAllSeenBlocks(Direction.BOTTOM, 1),
			((1,3,0), (1,2,0), (2,1,1), (3,1,1))
		)
		self.assertEqual(
			# From Right on column with ID 3
			solve.getAllSeenBlocks(Direction.RIGHT, 3),
			((3,2,1), (3,1,1), (2,0,1), (1,0,1))
		)
		self.assertEqual(
			# From Top on column with ID 2
			solve.getAllSeenBlocks(Direction.TOP, 2),
			((2,0,0), (2,1,0), (3,2,1))
		)

	def test_setTo0Blocks(self):
		self.assertEqual(
			sorted(tuple(Solve(Board.parseGameID("4x4:5,3,2,aLcRLcLLaLb,3,2,1,0,0,1,2,2,3,1,0,3,1,3,2,0")).setTo0Blocks())),
			sorted((
				(0, 0, Block.GHOST.value),
				(2, 0, Block.GHOST.value),
				(3, 0, Block.GHOST.value),
				(3, 1, Block.GHOST.value),
				(0, 1, Block.VAMPIRE.value),
				(0, 3, Block.VAMPIRE.value)
			))
		)

	def test_setToLimitedBlocks(self):
		board = Board.parseGameID("4x4:3,2,7,cRLaRhR,3,3,3,3,3,3,2,0,0,0,3,2,3,2,2,3")
		board._map[2][1] = Block.GHOST.value
		solve = Solve(board)
		result1 = solve.setToLimitedBlocks()
		self.assertEqual(
			sorted(result1),
			sorted((
				(0, 0, {Block.ZOMBIE.value}),
				(0, 2, {Block.ZOMBIE.value}),
				(0, 3, {Block.ZOMBIE.value}),
				(1, 0, {Block.ZOMBIE.value}),
				(1, 1, {Block.ZOMBIE.value}),
				(1, 3, {Block.ZOMBIE.value, Block.VAMPIRE.value}),
				(2, 0, {Block.ZOMBIE.value}),
				(2, 2, {Block.GHOST.value}),
				(2, 3, {Block.GHOST.value}),
				(3, 1, {Block.VAMPIRE.value})
			))
		)
		solve.appendNewPossibles(((x[0], x[1]), x[2]) for x in result1)
		solve.searchAndSetOnlyOnePossible()
		result2 = solve.setToLimitedBlocks()
		self.assertEqual(
			sorted(result2),
			sorted((
				(3, 2, {Block.ZOMBIE.value}),
				(1, 3, {Block.ZOMBIE.value, Block.VAMPIRE.value})
			))
		)
		solve.appendNewPossibles(((x[0], x[1]), x[2]) for x in result2)
		solve.searchAndSetOnlyOnePossible()
		result3 = solve.setToLimitedBlocks()
		self.assertEqual(
			sorted(result3),
			sorted((
				(1, 3, {Block.VAMPIRE.value}),
			))
		)





















































if __name__ == "__main__":
	unittest.main()