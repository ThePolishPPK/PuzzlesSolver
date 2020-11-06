#include "./Board.h"

#ifndef SGT_UNDEAD_SOLVE_HEADER
#define SGT_UNDEAD_SOLVE_HEADER

namespace sgt {
namespace undead {
	class Solve {
	public:
		Solve(Board* board);
		unsigned char getCountOfGhostsLeft();
		unsigned char getCountOfVampiresLeft();
		unsigned char getCountOfZombiesLeft();

	private:
		Board* board;
	};
};
};

#endif
