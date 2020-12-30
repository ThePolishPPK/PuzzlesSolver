#include <gtest/gtest.h>
#include "../Board.h"
#include <stdexcept>
#include <string>
#include <sstream>

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

TEST(BoardTest, exportSave) {
	char gameID[] = "5x5:1/1/3/4/1.2/2/1/3/3/1.1.1";
	Board board = Board::parseGameID(gameID);
	board.getBlock(0, 0).changeType(Type::White);
	board.getBlock(1, 0).changeType(Type::White);
	board.getBlock(2, 0).changeType(Type::White);
	board.getBlock(0, 1).changeType(Type::White);
	board.getBlock(1, 1).changeType(Type::White);
	board.getBlock(2, 1).changeType(Type::White);
	board.getBlock(0, 4).changeType(Type::Black);
	board.getBlock(1, 4).changeType(Type::White);
	board.getBlock(2, 4).changeType(Type::Black);
	board.getBlock(3, 4).changeType(Type::White);
	board.getBlock(4, 4).changeType(Type::Black);
	board.getBlock(3, 0).changeType(Type::Black);
	board.getBlock(3, 1).changeType(Type::Black);
	board.getBlock(3, 2).changeType(Type::Black);
	board.getBlock(3, 3).changeType(Type::Black);
	board.getBlock(2, 2).changeType(Type::Black);
    
	std::string expect("SAVEFILE:41:Simon Tatham's Portable Puzzle Collection\nVERSION :1:1\nGAME    :7:Pattern\nPARAMS  :3:5x5\nCPARAMS :3:5x5\nDESC    :25:1/1/3/4/1.2/2/1/3/3/1.1.1\nNSTATES :2:17\nSTATEPOS:2:17\nMOVE    :8:E0,0,1,1\nMOVE    :8:E0,1,1,1\nMOVE    :8:F0,4,1,1\nMOVE    :8:E1,0,1,1\nMOVE    :8:E1,1,1,1\nMOVE    :8:E1,4,1,1\nMOVE    :8:E2,0,1,1\nMOVE    :8:E2,1,1,1\nMOVE    :8:F2,2,1,1\nMOVE    :8:F2,4,1,1\nMOVE    :8:F3,0,1,1\nMOVE    :8:F3,1,1,1\nMOVE    :8:F3,2,1,1\nMOVE    :8:F3,3,1,1\nMOVE    :8:E3,4,1,1\nMOVE    :8:F4,4,1,1\n");
	ASSERT_EQ(board.exportSave(), expect);
};

TEST(BoardTest, exportGameID) {
	char gameID[] = "5x5:3/1.2/1.2/2/1/4/1/1/3/3";
	Board board = Board::parseGameID(gameID);
	ASSERT_EQ(board.exportGameID(), std::string(gameID));
};

TEST(BoardTest, parseSave) {
	char saveCorrect[] = "SAVEFILE:41:Simon Tatham's Portable Puzzle Collection\nVERSION :1:1\nGAME    :7:Pattern\nPARAMS  :5:20x20\nCPARAMS :5:20x20\nDESC    :246:1.2.7/1.1.1.4/1.3.1.6.2/9.3.4/5.3.1.1/7.3.1.1/6.5.1/3.5.2.1/4.3.2/3.1.2/5.1.3/3.1.1.5/3.5/3.6/1.3.5.1/9.2.1/11.3/4.5.1.1/3.4/2.2/4.7.4/1.7.4/10.5/5.1.1.5/5.2.2/6.5/4.12/1.2.8/2.2.5/1.1.2.3/1.1.3.3/7.2/6.2/4.4/1.1.5/1.1.5/2.3.4/4.3.2/4.1.2.1/2.4.4\nNSTATES :2:64\nSTATEPOS:2:64\nMOVE    :9:F2,11,1,1\nMOVE    :9:F2,12,1,1\nMOVE    :9:F2,13,1,1\nMOVE    :8:F3,0,1,1\nMOVE    :8:F3,1,1,1\nMOVE    :8:F3,2,1,1\nMOVE    :8:F3,3,1,1\nMOVE    :8:F3,4,1,1\nMOVE    :8:F3,5,1,1\nMOVE    :8:F3,6,1,1\nMOVE    :8:F3,7,1,1\nMOVE    :8:F3,8,1,1\nMOVE    :8:E3,9,1,1\nMOVE    :9:F3,12,1,1\nMOVE    :9:F3,16,1,1\nMOVE    :9:F3,17,1,1\nMOVE    :8:F4,2,1,1\nMOVE    :8:F5,2,1,1\nMOVE    :8:F5,5,1,1\nMOVE    :8:F5,6,1,1\nMOVE    :8:F6,2,1,1\nMOVE    :8:F7,2,1,1\nMOVE    :8:F8,0,1,1\nMOVE    :8:F8,1,1,1\nMOVE    :8:F8,2,1,1\nMOVE    :8:E8,4,1,1\nMOVE    :8:F8,6,1,1\nMOVE    :8:F9,0,1,1\nMOVE    :8:F9,1,1,1\nMOVE    :8:F9,2,1,1\nMOVE    :8:F9,6,1,1\nMOVE    :9:F10,0,1,1\nMOVE    :9:F10,1,1,1\nMOVE    :9:F10,2,1,1\nMOVE    :9:F10,3,1,1\nMOVE    :9:F10,4,1,1\nMOVE    :9:E10,5,1,1\nMOVE    :9:F10,6,1,1\nMOVE    :9:F11,0,1,1\nMOVE    :9:F11,1,1,1\nMOVE    :9:F11,2,1,1\nMOVE    :9:E11,3,1,1\nMOVE    :9:F11,6,1,1\nMOVE    :9:F12,6,1,1\nMOVE    :9:F12,7,1,1\nMOVE    :9:F13,6,1,1\nMOVE    :9:F14,6,1,1\nMOVE    :9:F15,2,1,1\nMOVE    :9:F15,6,1,1\nMOVE    :9:F15,7,1,1\nMOVE    :9:F15,8,1,1\nMOVE    :9:F16,0,1,1\nMOVE    :9:F16,1,1,1\nMOVE    :9:F16,2,1,1\nMOVE    :9:F16,3,1,1\nMOVE    :9:F16,4,1,1\nMOVE    :9:F16,5,1,1\nMOVE    :9:F16,6,1,1\nMOVE    :9:F16,7,1,1\nMOVE    :9:F16,8,1,1\nMOVE    :9:F16,9,1,1\nMOVE    :10:F16,10,1,1\nMOVE    :10:E16,11,1,1";
	std::stringstream saveCorrectStream(saveCorrect, std::stringstream::in);
	std::vector<std::vector<char>> blocksCorrect = {
		{0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0},
		{0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0},
		{0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0},
		{0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 1, 0, 0, 0},
		{0, 0, 0, 1, 0, 0, 0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0},
		{0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0},
		{0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0},
		{0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0},
		{0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0},
		{0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0},
		{0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0},
		{0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0}
	};
	std::string save("SAVEFILE:41:Simon Tatham's Portable Puzzle Collection\nVERSION :1:1\nGAME    :7:Pattern\nPARAMS  :3:7x7\nCPARAMS :3:7x7\nSEED    :15:730289631514132\nDESC    :41:2.2/2/1.1/1/5/1.5/1.4/3.2/2/2/3/5/1.3/1.3/3.1\nNSTATES :2:18\nSTATEPOS:2:18\nMOVE    :8:F6,5,1,1\nMOVE    :8:F5,4,1,1\nMOVE    :8:F4,6,1,1\nMOVE    :8:F5,6,1,1\nMOVE    :8:F4,5,1,1\nMOVE    :8:F0,0,1,1\nMOVE    :8:F2,0,1,1\nMOVE    :8:E2,4,1,1\nMOVE    :8:E4,2,1,1\nMOVE    :8:E2,2,1,1\nMOVE    :8:U2,4,1,1\nMOVE    :8:F1,4,1,1\nMOVE    :8:F5,0,1,1\nMOVE    :8:F6,0,1,1\nMOVE    :8:E6,1,1,1\nMOVE    :8:E5,1,1,1\nMOVE    :8:E4,1,1,1");
	
	std::vector<std::tuple<unsigned short, unsigned char, const char*, const char*>> changesToFail = {
		{197, 0, "/3.1", "Invalid description! Parameter 3.1 is additional!"},
		{30, 1, "n", "Invalid save file text!"},
		{76, 9, "6:Undead", "Invalid game name!"},
		{214, 1, "9", "Invalid NSTATES!"},
		{228, 1, "9", "Invalid state position!"},
		{462, 3, "9,6", "Invalid move (out of range)!"},
		{406, 3, "5,7", "Invalid move area!"},
		{97, 18, "3x5\nCPARAMS :3:7x8", "Invalid size of board!"},
		{126, 1, "4", "Invalid defined length of parameter (SEED)!"}
	};
	
	auto numToType = [](char num) {
		switch (num) {
			case (0):
				return Type::Empty;
			case (1):
				return Type::Black;
			default:
				return Type::White;
		};
	};
	auto typeToName = [](Type type) {
		switch (type) {
			case (Type::Empty):
				return "sgt::pattern::Type::Empty";
			case (Type::Black):
				return "sgt::pattern::Type::Black";
			default:
				return "sgt::pattern::Type::White";
		};
	};
	
	Board tempCorrect = Board::parseSave(saveCorrectStream);
	ASSERT_EQ(tempCorrect.width, 20) << "Invalid width!";
	ASSERT_EQ(tempCorrect.height, 20) << "Invalid height!";
	
	for (char y=0; y<20; y++) {
		for (char x=0; x<20; x++) {
			Type expectedType = numToType(blocksCorrect[y][x]);
			
			ASSERT_EQ(
				tempCorrect.getBlock(x, y).getType(),
				expectedType
			) << "Invalid type of block on x="
				<< std::to_string(x) << " and y="
				<< std::to_string(y) << ", expected type this is"
				<< typeToName(expectedType) << " got "
				<< typeToName(tempCorrect.getBlock(x, y).getType()) << ".";
		}
	}
	
	for (auto change=changesToFail.begin(); change != changesToFail.end(); change++) {
		std::string tempSave = save;
		tempSave.replace(
			std::get<0>(*change),
			std::get<1>(*change),
			std::get<2>(*change)
		);
		std::stringstream tempStream(tempSave, std::stringstream::in);
		
		ASSERT_THROW(
			Board::parseSave(tempStream),
			std::invalid_argument
		) << std::get<3>(*change);
	}
};
