#include <gtest/gtest.h>
#include "../Solve.h"
#include "../Board.h"

using namespace sgt::undead;

TEST(SolveTest, Constructor) {
	Board tempBoard(1, 1);
	Solve tempSolve(&tempBoard);
	std::vector<std::pair<			// Standard Monsters sequence = Ghost, Vampire, Zombie
		const char*,				// GameID
		std::array<unsigned char, 3>// Seen monsters in standard sequence
	>> simpleDataSet = {
		{"7x7:17,14,5,dLdLaRReLLfRaLdLaRgRaRRb,8,1,5,1,0,1,4,2,0,2,2,0,2,2,4,8,0,6,6,5,7,6,0,0,5,3,3,4", {17, 14, 5}},
		{"7x7:9,15,6,bLaRaRLaLRRdLaRhRaLaRLLdRbRcLLLa,3,5,0,1,0,3,7,5,4,1,0,4,1,3,1,1,0,1,6,0,4,2,2,3,5,2,2,2", {9, 15, 6}}
	};

	std::vector<std::tuple<
		const char*,					// GameID	
		std::array<unsigned char, 3>,	// Seen monsters in standard sequence
		std::array<						// Monster locations. Monsters are in standard sequence.
			std::vector<
				std::pair<unsigned char, unsigned char>
			>, 3>
	>> advancedDataSet = {
		{
			"4x4:4,1,4,LLbLLbRaRcRa,2,2,3,2,2,0,3,0,2,1,1,4,2,0,0,2",
			{2, 0, 1},
			{{
				{{2, 0}, {1, 2}},
				{{0, 3}},
				{{3, 2}, {2, 1}, {3, 3}}
			}}
		},
		{
			"5x5:2,11,4,cLaLbLRaLfLaLbRa,3,3,5,1,0,0,1,4,3,1,3,1,5,3,0,0,4,0,1,4",
			{2, 7, 1},
			{{
				{},
				{{0, 0}, {1, 4}, {3, 2}, {4, 4}},
				{{0, 2}, {4, 0}, {2, 3}}
			}}
		}
	};

	for (auto data=simpleDataSet.begin(); data != simpleDataSet.end(); data++) {
		tempBoard = Board::parseGameID(data->first);
		tempSolve = Solve(&tempBoard);
		ASSERT_EQ(tempSolve.getCountOfGhostsLeft(), data->second[0]);
		ASSERT_EQ(tempSolve.getCountOfVampiresLeft(), data->second[1]);
		ASSERT_EQ(tempSolve.getCountOfZombiesLeft(), data->second[2]);
	}

	for (auto data=advancedDataSet.begin(); data != advancedDataSet.end(); data++) {
		tempBoard = Board::parseGameID(std::get<0>(*data));
		tempSolve = Solve(&tempBoard);
		auto monsters = std::get<2>(*data);
		auto seenMonsters = std::get<1>(*data);

		for (unsigned char monsterID=0; monsterID<3; monsterID++) {
			for (auto block=monsters[monsterID].begin(); block != monsters[monsterID].end(); block++) {
				tempBoard.getBlock(
					block->first,
					block->second
				).changeType(
					(monsterID == 0)? Type::Ghost	:
					(monsterID == 1)? Type::Vampire	: Type::Zombie
				);
			}
		}
		ASSERT_EQ(tempSolve.getCountOfGhostsLeft(), seenMonsters[0]);
		ASSERT_EQ(tempSolve.getCountOfVampiresLeft(), seenMonsters[1]);
		ASSERT_EQ(tempSolve.getCountOfZombiesLeft(), seenMonsters[2]);
	}
};
