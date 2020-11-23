#include <gtest/gtest.h>
#include "../Board.h"
#include <stdexcept>
#include <cstdio>

using namespace sgt::pattern;

TEST(BoardTest, Constructor) {
	ASSERT_THROW(Board(0, 4), std::invalid_argument) << "Cannot create Board with width equal 0!";
	ASSERT_THROW(Board(3, 0), std::invalid_argument) << "Cannot create Board with height equal 0!";
	ASSERT_THROW(Board(0, 0), std::invalid_argument) << "Cannot create Board with sizes equal 0!";
	ASSERT_NO_THROW(Board(5, 12)) << "Width and Height is valid!";
};

TEST(BoardTest, parseGameID) {
	std::vector<std::tuple<
		const char*,	//GameID
		std::pair<unsigned char, unsigned char>,	// Width, Height
		std::array<
			std::vector<std::vector<unsigned char>>	// Sessions of black blocks
		, 2>
	>> testData{
		{"5x5:4/3/3/1/1/3/3/3/1/2", {5, 5}, {{ {{4}, {3}, {3}, {1}, {1}}, {{3}, {3}, {3}, {1}, {2}} }}},
		{
			"11x18:3/2.4/3.3/3.4/6.4.1/4.3/2.7.2/1.5.1.1/10.1/3.7.2.1/2.8.6/3.2/4.3/4.4/1.1.1.1/1.3/1.3/1.3/7/7/7/8/3.2/7.1/4.1.2/2.1.1.2/1/2.1/1.3",
			{11, 18},
			{{
				{{3}, {2,4}, {3,3}, {3,4}, {6,4,1}, {4,3}, {2,7,2}, {1,5,1,1}, {10,1}, {3,7,2,1}, {2,8,6}},
				{{3,2}, {4,3}, {4,4}, {1,1,1,1}, {1,3}, {1,3}, {1,3}, {7}, {7}, {7}, {8}, {3,2}, {7,1}, {4,1,2}, {2,1,1,2}, {1}, {2,1}, {1,3}}
			}}
		}
	};

	for (auto data=testData.begin(); data != testData.end(); data++) {
		auto sizes = std::get<1>(*data);
		auto sessionsColumn = std::get<2>(*data)[0];
		auto sessionsRow = std::get<2>(*data)[1];
		Board tempBoard = Board::parseGameID(const_cast<char*>(std::get<0>(*data)));
		ASSERT_EQ(tempBoard.width, sizes.first);
		ASSERT_EQ(tempBoard.height, sizes.second);

		for (unsigned char y=0; y < sizes.second; y++) {
			std::vector<unsigned char> sessions = tempBoard.getSessionsInRow(y);
			ASSERT_EQ(sessions, sessionsRow[y]) << "Invalid sessions on row, number: "+std::to_string(y)+"!";
		}
		for (unsigned char x=0; x < sizes.first; x++) {
			std::vector<unsigned char> sessions = tempBoard.getSessionsInColumn(x);
			ASSERT_EQ(sessions, sessionsColumn[x])  << "Invalid sessions on column, number: "+std::to_string(x)+"!";
		}
	}
};

TEST(BoardTest, getBlock) {
	Board tempBoard(14, 16);
	ASSERT_NO_THROW(tempBoard.getBlock(13, 7));
	ASSERT_NO_THROW(tempBoard.getBlock(0, 2));
	ASSERT_NO_THROW(tempBoard.getBlock(13, 15));
	ASSERT_NO_THROW(tempBoard.getBlock(0, 0));
	ASSERT_NO_THROW(tempBoard.getBlock(5, 9));

	ASSERT_THROW(tempBoard.getBlock(14, 9), std::invalid_argument);
	ASSERT_THROW(tempBoard.getBlock(14, 16), std::invalid_argument);
	ASSERT_THROW(tempBoard.getBlock(12, 16), std::invalid_argument);
	ASSERT_THROW(tempBoard.getBlock(45, 23), std::invalid_argument);
	ASSERT_THROW(tempBoard.getBlock(33, 16), std::invalid_argument);
	ASSERT_THROW(tempBoard.getBlock(14, 76), std::invalid_argument);
};

TEST(BoardTest, getSessionsInColumnAndRow) {
	Board tempBoard(18, 11);
	ASSERT_NO_THROW(tempBoard.getSessionsInColumn(4));
	ASSERT_NO_THROW(tempBoard.getSessionsInColumn(17));
	ASSERT_NO_THROW(tempBoard.getSessionsInColumn(14));
	ASSERT_NO_THROW(tempBoard.getSessionsInColumn(0));
	ASSERT_NO_THROW(tempBoard.getSessionsInColumn(2));
	ASSERT_NO_THROW(tempBoard.getSessionsInRow(6));
	ASSERT_NO_THROW(tempBoard.getSessionsInRow(10));
	ASSERT_NO_THROW(tempBoard.getSessionsInRow(7));
	ASSERT_NO_THROW(tempBoard.getSessionsInRow(0));
	ASSERT_NO_THROW(tempBoard.getSessionsInRow(9));

	ASSERT_THROW(tempBoard.getSessionsInColumn(18), std::invalid_argument);
	ASSERT_THROW(tempBoard.getSessionsInColumn(23), std::invalid_argument);
	ASSERT_THROW(tempBoard.getSessionsInColumn(45), std::invalid_argument);
	ASSERT_THROW(tempBoard.getSessionsInRow(11), std::invalid_argument);
	ASSERT_THROW(tempBoard.getSessionsInRow(97), std::invalid_argument);
	ASSERT_THROW(tempBoard.getSessionsInRow(22), std::invalid_argument);
};
