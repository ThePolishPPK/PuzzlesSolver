#include "Solve.h"
#include "Block.h"
#include "Type.cpp"
#include <cstdio>

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
	 * @todo	Optimize function. Ex add to one loop
	 */
	std::vector<solvedBlock_t> Solve::getMaxDeparturedBlocks() {
		std::vector<solvedBlock_t> output = {};
		std::vector<
			std::vector<bool>
		> alreadySet(this->_board.height, std::vector<bool>(this->_board.width, false));

		// Rows
		for (unsigned char y=0; y < this->_board.height; y++) {
			auto sessions = this->_board.getSessionsInRow(y);
			unsigned char delta = this->_board.width - (sessions.size()-1);
			for (auto session = sessions.begin(); session != sessions.end(); session++) {
				delta -= (*session);
			}
			unsigned char offset = 0;
			for (auto session = sessions.begin(); session != sessions.end(); session++) {
				for (unsigned char x = offset+delta; x < offset+(*session); x++) {
					if (! alreadySet[y][x]) {
						alreadySet[y][x] = true;
						output.push_back(
							solvedBlock_t(x, y, Type::Black)
						);
					}
				}
				offset += (*session);
			}
		}

		// Columns
		for (unsigned char x=0; x < this->_board.width; x++) {
			auto sessions = this->_board.getSessionsInColumn(x);
			unsigned char delta = this->_board.height - (sessions.size()-1);
			for (auto session = sessions.begin(); session != sessions.end(); session++) {
				delta -= (*session);
			}
			unsigned char offset = 0;
			for (auto session = sessions.begin(); session != sessions.end(); session++) {
				for (unsigned char y = offset+delta; y < offset+(*session); y++) {
					if (! alreadySet[y][x]) {
						alreadySet[y][x] = true;
						output.push_back(
							solvedBlock_t(x, y, Type::Black)
						);
					}
				}
				offset += (*session);
			}
		}
		return output;
	};

	/**
	 * @brief	Method complete blocks on start and end of line.
	 * @details
	 * Method search @ref Type "black" @ref Block "blocks" on start or end of line and fill with session length and close.
	 * If cont of sessions are lower or equal than fill other blocks with white blocks.
	 * @returns	Vector of @ref solvedBlock_t "solved blocks"
	 * @todo	Method
	 * @todo	Test
	 */
	std::vector<solvedBlock_t> Solve::getComplementaryBlocks() {
	
	};

	solvedBlock_t::solvedBlock_t(unsigned char x, unsigned char y, Type type) {
		this->x = x;
		this->y = y;
		this->type = type;
	};
}
