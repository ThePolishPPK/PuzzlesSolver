#include "Solve.h"

/**
 * @author	ThePPK
 * @file
 */

namespace sgt::pattern {
	/**
	 * @class	Solve
	 * @brief	Class can operate on @ref Board to show certain Type
	 * @details
	 * Most of methods are steps of algorithm to solve @ref Board.
	 * @todo	Write unittests
	 */

	/**
	 * @brief	Constructor for @ref Solve class
	 * @param board Address for @ref Board to operate
	 * @todo	Make function
	 */
	Solve::Solve(Board& board) : _board(board) {
	
	};

	/**
	 * @brief	Method return data for certainty @ref Block "Blocks" by Type "Black" @ref Block sessions
	 * @details
	 * @todo	Make method
	 */
	std::vector<solvedBlock_t> Solve::getUnionOfOffsets() {
	
	};
}
