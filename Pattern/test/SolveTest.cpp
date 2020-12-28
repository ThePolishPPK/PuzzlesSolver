#include <gtest/gtest.h>
#include <vector>
#include "../Solve.h"
#include "../Board.h"
#include "../Type.cpp"

using namespace sgt::pattern;

TEST(SolveTest, getMaxDeparturedBlocks) {
	char gameID[] = "10x10:4.3/3.3/1.1.3/5/3.3/1.4/3.1/2.1/2.1.1/2.1.1.1/1.4/1.1.4/2.3/3.2/2/2.4/1.1/6/6/6.1";
	Board board = Board::parseGameID(gameID);
	Solve solve(board);
	std::vector<std::pair<char, char>> expected = {
		{0, 2}, {0, 3}, {0, 7},
		{2, 9},
		{3, 9},
		{4, 7}, {4, 8}, {4, 9},
		{5, 7}, {5, 8}, {5, 9},
		{6, 1}, {6, 5},
		{7, 1}
	};
	std::vector<solvedBlock_t> result = solve.getMaxDeparturedBlocks();
	ASSERT_EQ(result.size(), expected.size()) << "Method doesn't return enough count of elements!";
	for (auto block = expected.begin(); block != expected.end(); block++) {
		bool found = false;
		for (auto recived = result.begin(); recived != result.end(); recived++) {
			if (recived->x == block->first && recived->y == block->second) {
				found = true;
				ASSERT_EQ(recived->type, Type::Black) << "Block with x:"+std::to_string(block->first)
					+" and y:"+std::to_string(block->second)
					+" have invalid Type!";
				break;
			}
		}
		if (found == false) {
			FAIL() << "Block with x:"+std::to_string(block->first)
				+" and y:"+std::to_string(block->second)
				+" not found in result!";
		}
	}
}

TEST(SolveTest, getComplementaryBlocks) {
	// Preparing Board
	char gameID[] = "10x10:7/6/5.3/5.3/4.2/2.3.1/3/3/1/1.1/4.1/6/5/9/8.1/2.3/1/2/3.1/4";
	Board board = Board::parseGameID(gameID);
	std::vector<std::pair<char, char>> changes = {
		{2, 9}, {3, 9},
		{2, 0}, {3, 0}, {3, 2},
		{0, 5},
		{0, 2}, {4, 2},
		{0, 4},
		{9, 8}
	};
	std::vector<solvedBlock_t> expected = {
		{2, 1, Type::Black}, {2, 2, Type::Black}, {2, 3, Type::Black}, {2, 4, Type::Black}, {2, 5, Type::White}, {2, 6, Type::White}, {2, 7, Type::Black}, {2, 8, Type::Black},
		{3, 1, Type::Black}, {3, 3, Type::Black}, {3, 4, Type::Black}, {3, 5, Type::White}, {3, 6, Type::White}, {3, 7, Type::Black}, {3, 8, Type::Black},
		{1, 5, Type::Black},
		{1, 2, Type::Black}, {5, 2, Type::White},
		{1, 4, Type::Black}, {4, 4, Type::Black}, {5, 4, Type::Black}, {6, 4, Type::Black}, {7, 4, Type::Black}, {8, 4, Type::White},
		{8, 8, Type::White}
	};
	for (auto change = changes.begin(); change != changes.end(); change++) {
		board.getBlock(
			(*change).first,
			(*change).second
		).changeType(Type::Black);
	}

	// Test
	Solve solve(board);
	std::vector<solvedBlock_t> result = solve.getComplementaryBlocks();

	ASSERT_EQ(result.size(), expected.size()) << "Method doesn't return enough count of elements!";
	for (auto block = expected.begin(); block != expected.end(); block++) {
		bool found = false;
		for (auto recived = result.begin(); recived != result.end(); recived++) {
			if (recived->x == block->x && recived->y == block->y) {
				found = true;
				ASSERT_EQ(recived->type, block->type) << "Block with x:"+std::to_string(block->x)
					+" and y:"+std::to_string(block->y)
					+" have invalid Type!";
				break;
			}
		}
		if (found == false) {
			FAIL() << "Block with x:"+std::to_string(block->x)
				+" and y:"+std::to_string(block->y)
				+" not found in result!";
		}
	}
}

TEST(SolveTest, appendSolvedBlocks) {
	char gameID[] = "5x5:1/4/1.2/2/2/3/1.2/1/3/2";
	Board board = Board::parseGameID(gameID);
	Solve solve(board);
	std::vector<solvedBlock_t> solvedBlocks = {
		{3, 4, Type::White},
		{0, 0, Type::Black},
		{1, 2, Type::Black},
		{2, 0, Type::White}
	};
	solve.appendSolvedBlocks(solvedBlocks);
	for (auto expected = solvedBlocks.begin(); expected != solvedBlocks.end(); expected++) {
		ASSERT_EQ(board.getBlock(expected->x, expected->y).getType(), expected->type);
	}
}
