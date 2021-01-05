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
	Solve::Solve(Board& board) : _board(board) {};

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
				offset += (*session)+1;
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
				offset += (*session)+1;
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
	 * @todo	Clear code
	 */
	std::vector<solvedBlock_t> Solve::getComplementaryBlocks() {
		std::vector<solvedBlock_t> output = {};
		std::vector<std::vector<bool>> alreadySet(
			this->_board.height,
			std::vector<bool>(this->_board.width, false)
		);
		unsigned char length = this->_board.height;
		unsigned char count = this->_board.width;
		bool column = true;
		for (unsigned char x=0; x <= count; x++) {
			if (x == count) {
				if (column) {
					column = false;
					count = this->_board.height;
					length = this->_board.width;
					x = 0;
				} else {
					break;
				}
			}
			unsigned char setFirst, setLast;
			auto sessions = column ? this->_board.getSessionsInColumn(x) : this->_board.getSessionsInRow(x);
			setFirst = (this->_board.getBlock(column? x : 0, column? 0 : x).getType() == Type::Black)? sessions[0] : 0;
			setLast = length;
			if (this->_board.getBlock(column? x : length-1, column? length-1 : x).getType() == Type::Black and
				sessions.size() >= 2) {
				setLast -= sessions.back()+1;
			}
			for (unsigned char y=0; y < length; y++) {
				if (setFirst == 0 or y > setFirst) {
					y = setLast;
					setFirst = length;
					if (y >= length) { break; }
				}
				if (not alreadySet[y][x] and this->_board.getBlock(column? x : y, column? y : x).getType() == Type::Empty) {
					if (y == setFirst or y == setLast) {
						output.push_back(
							solvedBlock_t(column? x : y, column? y : x, Type::White)
						);
					} else {
						output.push_back(
							solvedBlock_t(column? x : y, column? y : x, Type::Black)
						);
					}
				}
				alreadySet[column? x : y][column? y : x] = true;
			}
		}
		return output;
	};

	/**
	 * @breif	Method updata blocks.
	 * @details
	 * Method update blocks types by @ref solvedBlock_t "solved blocks" data.
	 * @param	Vector of @ref solvedBlock_t "solved blocks"
	 */
	void Solve::appendSolvedBlocks(std::vector<solvedBlock_t> solvedBlocks) {
		for (auto block = solvedBlocks.begin(); block != solvedBlocks.end(); block++) {
			this->_board.getBlock(block->x, block->y).changeType(block->type);
		}
	};

	solvedBlock_t::solvedBlock_t(unsigned char x, unsigned char y, Type type) {
		this->x = x;
		this->y = y;
		this->type = type;
	};

	/**
	 * @brief	Method fill @ref Type "empty" @ref Block "blocks" in line if already solved
	 * @details
	 * Method scan line and count used black blocks. When count of black blocks is equal sum of sessions then all empty blocks make white.
	 * @return	All missing white blocks in solved lines
	 */
	std::vector<solvedBlock_t> Solve::getFillingWhite() {
		std::vector<solvedBlock_t> output;
		std::vector<std::vector<bool>> alreadySet(this->_board.width, std::vector<bool>(this->_board.height, false));
		unsigned char offset, lineNumber;
		unsigned char* x = &offset;
		unsigned char* y = &lineNumber;
		bool scanningColumns = false;
		unsigned char offsetLength = this->_board.width;
		unsigned char linesCount = this->_board.height;
		for (lineNumber=0; lineNumber<=linesCount; lineNumber++) {
			if (lineNumber == linesCount) {
				if (not scanningColumns) {
					scanningColumns = true;
					lineNumber = 0;
					linesCount = this->_board.width;
					y = &offset;
					x = &lineNumber;
				} else {break;}
				
			}
			unsigned char blackBlocks = 0;
			unsigned char requiredBlackBlocks = 0;
			std::vector<std::pair<unsigned char, unsigned char>> allEmptyBlocks;
			std::vector<unsigned char> sessionsInLine;
			if (scanningColumns) {
				sessionsInLine = this->_board.getSessionsInColumn(*x);
			} else {
				sessionsInLine = this->_board.getSessionsInRow(*y);
			}
			for (auto& session : sessionsInLine)
				requiredBlackBlocks += session;
			
			for (offset=0; offset<offsetLength; offset++) {
				Block block = this->_board.getBlock(*x, *y);
				if (block.getType() == Type::Black) {
					blackBlocks++;
				} else if (block.getType() == Type::Empty) {
					allEmptyBlocks.push_back({*x, *y});
				}
			}
			if (blackBlocks == requiredBlackBlocks) {
				for (auto& block : allEmptyBlocks) {
					if (not alreadySet[block.first][block.second]) {
						alreadySet[block.first][block.second] = true;
						output.push_back({block.first, block.second, Type::White});
					}
				}
			}
		}
		return output;
	};
}
