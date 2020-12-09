#include "Solve.h"
#include "Block.h"
#include "Type.cpp"

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
	 * @todo	Reflect about unordered lists to get solved blocks
	 */

	/**
	 * @brief	Constructor for @ref Solve class
	 * @param board Address for @ref Board to operate
	 */
	Solve::Solve(Board& board) : _board(board) {
	
	};

	/**
	 * @brief	Method search shadred blocks on hem offsets
	 * @details
	 * Method search certainty @ref Block "blocks" by sessions of @ref Type "black" blocks.
	 * Certainty @ref Block "blocks" are shared by this same blocks on virtual line with maximum and minimum offsets.
	 * You can see @ref Shared_blocks_of_max_offsets "example".
	 * @returns	Vector of @ref solvedBlock_t "solved type" @ref Block "block"
	 * @todo	Make method
	 */
	std::vector<solvedBlock_t> Solve::getMaxDeparturedBlocks() {
	};

	solvedBlock_t::solvedBlock_t(unsigned char x, unsigned char y, Type type) {
		this->x = x;
		this->y = y;
		this->type = type;
	};
}