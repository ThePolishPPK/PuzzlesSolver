from _solve import Block

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

Board2_4x4 = (
	( (1, Block.DIRECTION_BOTTOM_RIGHT), (None, Block.DIRECTION_RIGHT), (None, Block.DIRECTION_BOTTOM), (None, Block.DIRECTION_BOTTOM_LEFT) ),
	( (None, Block.DIRECTION_BOTTOM), (2, Block.DIRECTION_TOP), (None, Block.DIRECTION_LEFT), (None, Block.DIRECTION_BOTTOM_LEFT) ),
	( (None, Block.DIRECTION_RIGHT), (None, Block.DIRECTION_TOP_RIGHT), (None, Block.DIRECTION_BOTTOM), (None, Block.DIRECTION_TOP) ),
	( (None, Block.DIRECTION_RIGHT), (None, Block.DIRECTION_TOP), (None, Block.DIRECTION_TOP_RIGHT), (16, None) ),
)
Solution2_4x4 = (
	(1, 3, 4, 14),
	(6, 2, 5, 11),
	(7, 13, 8, 10),
	(15, 12, 9, 16)
)

TestLinks1 = (
	( (1, Block.DIRECTION_BOTTOM_RIGHT), (3, Block.DIRECTION_RIGHT), (4, Block.DIRECTION_BOTTOM), (14, Block.DIRECTION_BOTTOM_LEFT) ),
	( (6, Block.DIRECTION_BOTTOM), (2, Block.DIRECTION_TOP), (None, Block.DIRECTION_LEFT), (11, Block.DIRECTION_BOTTOM_LEFT) ),
	( (None, Block.DIRECTION_RIGHT), (None, Block.DIRECTION_TOP_RIGHT), (8, Block.DIRECTION_BOTTOM), (None, Block.DIRECTION_TOP) ),
	( (15, Block.DIRECTION_RIGHT), (None, Block.DIRECTION_TOP), (None, Block.DIRECTION_TOP_RIGHT), (16, None) ),
)

TestLinks1_NotLinking = (
	(False, False, True, False),
	(True, False, True, True),
	(True, True, True, True),
	(False, True, True, False)
)

TestLinks1_NotLinked = (
	(False, False, False, True),
	(True, False, True, True),
	(True, True, True, True),
	(False, True, True, False)
)
