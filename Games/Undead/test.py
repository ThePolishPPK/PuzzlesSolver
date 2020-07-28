import unittest
from _solve import Board, Solve

class TestBoard(unittest.TestCase):
	def test_parseGameID(self):
		parsed = Board.parseGameID("4x4:3,4,2,LaLReLLaRaRa,2,3,0,0,3,3,1,1,1,1,0,2,0,2,3,0")
		self.assertEqual(
			tuple(tuple(row) for row in parsed._map),
			(
				(Board.MIRROR_LEFT, Board.EMPTY, Board.MIRROR_LEFT, Board.MIRROR_RIGHT),
				(Board.EMPTY, Board.EMPTY, Board.EMPTY, Board.EMPTY),
				(Board.EMPTY, Board.MIRROR_LEFT, Board.MIRROR_LEFT, Board.EMPTY),
				(Board.MIRROR_RIGHT, Board.EMPTY, Board.MIRROR_RIGHT, Board.EMPTY)
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
			solve.getAllSeenBlocks(3, 1),
			((1,2,1),)
		)
		self.assertEqual(
			# From Left on column with ID 0
			solve.getAllSeenBlocks(3, 0),
			((1,0,1),)
		)
		self.assertEqual(
			# From Bottom on column with ID 1
			solve.getAllSeenBlocks(2, 1),
			((1,3,0), (1,2,0), (2,1,1), (3,1,1))
		)
		self.assertEqual(
			# From Right on column with ID 3
			solve.getAllSeenBlocks(1, 3),
			((3,2,1), (3,1,1), (2,0,1), (1,0,1))
		)
		self.assertEqual(
			# From Top on column with ID 2
			solve.getAllSeenBlocks(0, 2),
			((2,0,0), (2,1,0), (3,2,1))
		)
























































if __name__ == "__main__":
	unittest.main()