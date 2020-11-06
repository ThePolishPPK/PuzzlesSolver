#include "../Board.h"
#include "../Direction.cpp"
#include "../Type.cpp"
#include "../Block.cpp"
#include <math.h>
#include <gtest/gtest.h>
#include <stdexcept>
#include <tuple>

using namespace sgt::undead;


TEST(BoardTest, Constructor) {
	Board obj(10, 5);

	// Defined board sizes
	ASSERT_EQ(5, obj.Height) << "Height must be exactly equal second parameter in constructor!";
	ASSERT_EQ(10, obj.Width) << "Width must be exactly equal first parameter in constructor!";

	// Default values
	EXPECT_EQ(0, obj.Ghosts) << "Ghosts count by default should be 0!";
	EXPECT_EQ(0, obj.Vampires) << "Vampires count by default should be 0!";
	EXPECT_EQ(0, obj.Zombies) << "Zombies count by default should be 0!";

	bool throwExcept = false;

	// Check minimum board size parameters
	int args[2];
	for (unsigned char x=0; x<16; x++) {
		throwExcept = false;
		args[x%2] = std::rand() % 12;
		args[(x+1)%2] = (x%5)? 0 : -(std::rand()%12);

		try {
			Board(args[0], args[1]);
		} catch (const std::invalid_argument& err) {
			throwExcept = true;
		}
		ASSERT_TRUE(throwExcept) << "Constructor doesn't throw exception of Width or/and Height lower than 1! Tested for width=" << args[0] << " and height=" << args[1] << "!";
	}

	// Check maximum board size parameters
	for (unsigned char x=0; x<16; x++) {
		throwExcept = false;
		args[0] = (std::rand() % 12)+((x%2)? 13 : 1);
		args[1] = (std::rand() % 12)+(((x+1)%2)? 13 : 1);
		
		if (std::rand() % 5 == 0) {
			args[(x+1)%2] += 13;
		}

		try {
			Board(args[0], args[1]);
		} catch (const std::invalid_argument& err) {
			throwExcept = true;
		}
		ASSERT_TRUE(throwExcept) << "Maximum Board size that is 12 width and 12 height! Tested for width=" << args[0] << " and height=" << args[1] << "!";
	}
}

TEST(BoardTest, getBlock) {
	// Test created map
	unsigned char x,y;
	Board test(
		(std::rand() % 4) + 8,
		(std::rand() % 4) + 8
	);
	Block* tempBlock;
	
	for (x=0; x<test.Width; x++) {
		for (y=0; y<test.Height; y++) {
			tempBlock = &test.getBlock(x, y);
			ASSERT_EQ(tempBlock->x, x);
			ASSERT_EQ(tempBlock->y, y);
			ASSERT_EQ(tempBlock->BlockType, Type::Empty);
		}
	}
	
	std::vector<std::pair<char, char>> parameters = {
		{std::rand()%test.Width, test.Height},
		{test.Width, std::rand()%test.Height},
		{-1, 4},
		{-87, 2},
		{3, 43},
		{7, -76}
	};
	
	for (auto i = parameters.begin(); i != parameters.end(); i++) {
		ASSERT_DEATH(test.getBlock(i->first, i->second), "");
	}
}

TEST(BoardTest, parseGameID) {
	unsigned char x, y;
	Board tempBoard(1, 1);
	Block* tempBlock;

	// Data set
	std::vector<
		std::tuple<
			const char*,
			std::vector<std::vector<Type>>,
			std::vector<std::vector<unsigned char>>,
			std::pair<unsigned char, unsigned char>,
			std::vector<unsigned char>
	>> DataSet = {
		{
			// GameID
			"4x4:4,3,2,aRaRdRRLbLaL,1,1,1,2,0,3,2,0,2,1,1,1,0,2,3,0",
			// Type map
			{
				{Type::Empty, Type::MirrorRight, Type::Empty, Type::MirrorRight},
				{Type::Empty, Type::Empty, Type::Empty, Type::Empty},
				{Type::MirrorRight, Type::MirrorRight, Type::MirrorLeft, Type::Empty},
				{Type::Empty, Type::MirrorLeft, Type::Empty, Type::MirrorLeft},
			},
			// Seen monsters
			{
				{1, 1, 1, 2}, // Top
				{0, 3, 2, 0}, // Right
				{1, 1, 1, 2}, // Bottom
				{0, 3, 2, 0}, // Left
			},
			// Board size
			{4, 4},
			// Monsters count
			{4, 3, 2} // [Ghost, Vampire, Zombie]
		},
		{
			"4x4:1,4,4,dRaLRaLcLRR,1,3,2,2,4,0,2,0,0,0,1,4,1,4,0,4",
			{
				{Type::Empty, Type::Empty, Type::Empty, Type::Empty},
				{Type::MirrorRight, Type::Empty, Type::MirrorLeft, Type::MirrorRight},
				{Type::Empty, Type::MirrorLeft, Type::Empty, Type::Empty},
				{Type::Empty, Type::MirrorLeft, Type::MirrorRight, Type::MirrorRight},
			},
			{
				{1, 3, 2, 2},
				{4, 0, 2, 0},
				{4, 1, 0, 0},
				{4, 0, 4, 1},
			},
			{4, 4},
			{1, 4, 4}
		},
		{
			"4x4:2,5,4,dLcRaLcLR,2,3,3,3,3,3,0,0,0,2,3,4,2,0,0,3",
			{
				{Type::Empty, Type::Empty, Type::Empty, Type::Empty},
				{Type::MirrorLeft, Type::Empty, Type::Empty, Type::Empty},
				{Type::MirrorRight, Type::Empty, Type::MirrorLeft, Type::Empty},
				{Type::Empty, Type::Empty, Type::MirrorLeft, Type::MirrorRight},
			},
			{
				{2, 3, 3, 3},
				{3, 3, 0, 0},
				{4, 3, 2, 0},
				{3, 0, 0, 2},
			},
			{4, 4},
			{2, 5, 4}
		},
		{
			"5x5:8,3,4,aRRRaRdRfLaRLLbR,0,1,3,5,5,4,0,5,3,0,0,3,3,4,0,0,0,4,1,0",
			{
				{Type::Empty, Type::MirrorRight, Type::MirrorRight, Type::MirrorRight, Type::Empty},
				{Type::MirrorRight, Type::Empty, Type::Empty, Type::Empty, Type::Empty},
				{Type::MirrorRight, Type::Empty, Type::Empty, Type::Empty, Type::Empty},
				{Type::Empty, Type::Empty, Type::MirrorLeft, Type::Empty, Type::MirrorRight},
				{Type::MirrorLeft, Type::MirrorLeft, Type::Empty, Type::Empty, Type::MirrorRight}
			},
			{
				{0, 1, 3, 5, 5},
				{4, 0, 5, 3, 0},
				{0, 4, 3, 3, 0},
				{0, 1, 4, 0, 0},
			},
			{5, 5},
			{8, 3, 4}
		},
		{
			"7x7:1,13,12,dRaRcRaLaLaRLRdLaLcLRcLRRRLRbLaRLaLR,4,4,5,2,4,2,5,1,2,3,3,1,2,0,0,0,3,0,0,6,0,0,0,1,5,0,4,4",
			{
				{Type::Empty, Type::Empty, Type::Empty, Type::Empty, Type::MirrorRight, Type::Empty, Type::MirrorRight},
				{Type::Empty, Type::Empty, Type::Empty, Type::MirrorRight, Type::Empty, Type::MirrorLeft, Type::Empty},
				{Type::MirrorLeft, Type::Empty, Type::MirrorRight, Type::MirrorLeft, Type::MirrorRight, Type::Empty, Type::Empty},
				{Type::Empty, Type::Empty, Type::MirrorLeft, Type::Empty, Type::MirrorLeft, Type::Empty, Type::Empty},
				{Type::Empty, Type::MirrorLeft, Type::MirrorRight, Type::Empty, Type::Empty, Type::Empty, Type::MirrorLeft},
				{Type::MirrorRight, Type::MirrorRight, Type::MirrorRight, Type::MirrorLeft, Type::MirrorRight, Type::Empty, Type::Empty},
				{Type::MirrorLeft, Type::Empty, Type::MirrorRight, Type::MirrorLeft, Type::Empty, Type::MirrorLeft, Type::MirrorRight}
			},
			{
				{4, 4, 5, 2, 4, 2, 5},
				{1, 2, 3, 3, 1, 2, 0},
				{0, 6, 0, 0, 3, 0, 0},
				{4, 4, 0, 5, 1, 0, 0},
			},
			{7, 7},
			{1, 13, 12}
		}
	};
	
	for (auto data=DataSet.begin(); data != DataSet.end(); data++) {
		tempBoard = Board::parseGameID(std::get<0>(*data));
		auto map = std::get<1>(*data);
		auto seenMonsters = std::get<2>(*data);
		auto monstersList = std::get<4>(*data);

		ASSERT_EQ(tempBoard.Width, std::get<3>(*data).first) << "Wrong board width!";
		ASSERT_EQ(tempBoard.Height, std::get<3>(*data).second) << "Wrong board height!";
		ASSERT_EQ(tempBoard.Ghosts, monstersList[0]) << "Wrong Ghosts count!!";
		ASSERT_EQ(tempBoard.Vampires, monstersList[1]) << "Wrong Vampire count!!";
		ASSERT_EQ(tempBoard.Zombies, monstersList[2]) << "Wrong Zombie count!!";

		for (x=0; x<tempBoard.Width; x++) {
			ASSERT_EQ(tempBoard.SeenFromTop[x], seenMonsters[0][x]) << "Wrong count of seen monsters for Top! Column x=" << std::to_string(x) << "!";
			ASSERT_EQ(tempBoard.SeenFromBottom[x], seenMonsters[2][x]) << "Wrong count of seen monsters for Bottom! Column x=" << std::to_string(x) << "!";
		}

		for (y=0; x<tempBoard.Height; y++) {
			ASSERT_EQ(tempBoard.SeenFromRight[y], seenMonsters[1][y]) << "Wrong count of seen monsters for Right! Row y=" << std::to_string(y) << "!";
			ASSERT_EQ(tempBoard.SeenFromLeft[y], seenMonsters[3][y]) << "Wrong count of seen monsters for Left! Row y=" << std::to_string(y) << "!";
		}

		for (x=0; x<tempBoard.Width; x++) {
			for (y=0; y<tempBoard.Height; y++) {
				tempBlock = &tempBoard.getBlock(x, y);

				ASSERT_EQ(tempBlock->BlockType, map[y][x]) << "Wrong Block Type on x=" << std::to_string(x) << " and y=" << std::to_string(y) << "!";
				ASSERT_EQ(tempBlock->x, x) << "Wrong x coordinate!";
				ASSERT_EQ(tempBlock->y, y) << "Wrong y coordinate!";
			}
		}
	}
}

TEST(BoardTest, getAllSeenBlocks) {
	std::vector<std::tuple<
		const char*,
		std::vector<std::tuple<unsigned char, unsigned char, bool>>,
		std::pair<unsigned char, Direction>
	>> DataSet = {
		{
			// GameID
			"4x4:4,2,6,LaLgRLd,4,2,1,2,1,3,1,2,0,2,2,3,2,4,3,3",
			// List of seen blocks
			{{0, 2, true}, {1, 2, true}, {3, 1, false}, {1, 0, false}},
			// Location
			{2, Direction::LEFT}
		},
		{
			"7x7:7,16,3,aRRRbRLLcRbLLReRRaRLaRaRRRRbRaRgRL,2,1,1,0,5,2,0,0,3,4,0,0,3,0,0,0,0,2,4,2,3,3,2,1,1,3,3,0",
			{{6, 1, true}, {5, 2, false}, {4, 3, false}, {2, 4, false}, {1, 5, false}, {1, 6, false}},
			{1, Direction::RIGHT}
		},
		{
			"7x7:8,17,6,LLeLLbLRdLaRbLfLRaLcLRRbRdRLa,2,3,5,0,2,2,6,4,3,2,4,4,1,2,1,0,0,2,4,0,3,3,2,5,0,4,2,3",
			{{1, 2, false}, {2, 3, false}, {3, 3, false}, {4, 3, false}, {5, 3, false}, {6, 3, false}},
			{0, Direction::LEFT}
		},
		{
			"7x7:8,14,7,LaRaRbLaLaLaReRaLbRaRLRbLdLbLaRLcLLa,0,5,0,0,4,6,3,3,0,1,0,3,1,4,1,4,3,4,5,2,0,0,2,0,0,4,3,3",
			{{1, 0, true}, {1, 1, true}, {1, 2, true}, {1, 3, true}, {1, 4, true}, {2, 5, false}, {3, 5, false}},
			{1, Direction::UP}
		},
		{
			"5x5:4,6,3,bLaRaRRLRRbRaRLbRLd,0,2,0,1,0,0,4,2,1,3,1,2,2,3,0,0,3,2,0,4",
			{{1, 6, true}, {1, 6, false}, {2, 6, false}, {3, 6, false}, {4, 6, false}, {5, 6, false}, {6, 6, false}},
			{1, Direction::DOWN}
		}
	};

	for (auto data=DataSet.begin(); data!=DataSet.end(); data++) {
		auto result = Board::parseGameID(std::get<0>(*data)).getAllSeenBlocks(
			std::get<2>(*data).second,
			std::get<2>(*data).first
		);
		auto path = &std::get<1>(*data);
		ASSERT_EQ(result.size(), path->size()) << "Invalid seen blocks path!";
		for (unsigned char i=0; i<path->size(); i++) {
			ASSERT_EQ(result[i].first->x, std::get<0>((*path)[i])) << "Invalid x coordinate in " << std::to_string(i) << " seen block!";
			ASSERT_EQ(result[i].first->y, std::get<1>((*path)[i])) << "Invalid y coordinate in " << std::to_string(i) << " seen block!";
			ASSERT_EQ(result[i].second, std::get<2>((*path)[i])) << "Invalid mirror bypass status!";
		}
	}
}
