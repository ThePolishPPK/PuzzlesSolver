import unittest, pudb
from _solve import Board, Block

class BoardTest(unittest.TestCase):
	def test_parseGameID(self):
		board = Board.parseGameID("10x10:1.3.1/3/5.3/1.5/7/4/3.1.2/3.2/2.2/2/1.1.4/1.4/5.2/3.1/6/3/5/4/3.3/1.3")
		self.assertEqual(
			board.inRow,
			(
				(1,1,4),
				(1,4),
				(5,2),
				(3,1),
				(6,),
				(3,),
				(5,),
				(4,),
				(3,3),
				(1,3)
			)
		)
		self.assertEqual(
			board.inColumn,
			(
				(1,3,1),
				(3,),
				(5,3),
				(1,5),
				(7,),
				(4,),
				(3,1,2),
				(3,2),
				(2,2),
				(2,)
			)
		)
























if __name__ == "__main__":
	unittest.main()