#ifndef SGT_PATTERN_SOLVE_H
#define SGT_PATTERN_SOLVE_H

#include "Board.h"
#include "Block.h"
#include <vector>

namespace sgt::pattern {
	struct solvedBlock_t {
		unsigned char x; //!< @copydoc Block::x
		unsigned char y; //!< @copydoc Block::y
		Type type; //!< New Type for solved @ref Block
		solvedBlock_t(unsigned char x, unsigned char y, Type type);
	};

	class Solve {
	public:
		Solve(Board& board);
		std::vector<solvedBlock_t> getMaxDeparturedBlocks();

	private:
		const Board& _board; //!< Contain address for Board to solve
	};
}
#endif
