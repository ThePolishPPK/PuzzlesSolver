#include <gtest/gtest.h>
#include "../Solve.h"
#include "../Board.h"

using namespace sgt::undead;

TEST(SolveTest, Constructor) {
	Board tempBoard(1, 1);
	Solve tempSolve(&tempBoard);
	std::vector<std::pair<
		const char*,
		std::vector<unsigned char> > > simpleDataSet = {
		{"7x7:17,14,5,dLdLaRReLLfRaLdLaRgRaRRb,8,1,5,1,0,1,4,2,0,2,2,0,2,2,4,8,0,6,6,5,7,6,0,0,5,3,3,4", {17, 14, 5}},
		{"7x7:9,15,6,bLaRaRLaLRRdLaRhRaLaRLLdRbRcLLLa,3,5,0,1,0,3,7,5,4,1,0,4,1,3,1,1,0,1,6,0,4,2,2,3,5,2,2,2", {9, 15, 6}}
	};

	/* ToDo: Add method changing types of blocks to board class */
	for (auto data=simpleDataSet.begin(); data != simpleDataSet.end(); data++) {
		tempBoard = Board::parseGameID(data->first);
		tempSolve = Solve(&tempBoard);
		ASSERT_EQ(tempSolve.getCountOfGhostsLeft(), data->second[0]);
		ASSERT_EQ(tempSolve.getCountOfVampiresLeft(), data->second[1]);
		ASSERT_EQ(tempSolve.getCountOfZombiesLeft(), data->second[2]);
	}
};
