#include "Board.h"
#include "Block.h"
#include "Type.cpp"
#include <stdexcept>
#include <regex>

/**
 * @author ThePPK
 * @file
 */

namespace sgt::pattern {
	/**
	 * @class Board
	 * @brief	Parse GameID and store @ref Block "Blocks"
	 * @details
	 * Class store all @ref Block "Blocks" and all sessions of Black @ref Block "Blocks".
	 * Contain too @ref Board::parseGameID "method" parsing GameID to @ref Board.
	 */

	/**
	 * @brief	Constructor for @ref Board class
	 * @param width @copydoc Board::width
	 * @param height @copydoc Board::height
	 * @throw	std::invalid_argument When @p width or @p height equal zero
	 */
	Board::Board(unsigned char width, unsigned char height) : width(width), height(height) {
		if (width <= 0 || height <= 0) {
			throw std::invalid_argument("Width and/or Height can't be lower or equal zero!");
		}
		for (unsigned char y=0; y<height; y++) {
			this->_allocatedBlock.second.push_back(std::vector<unsigned char>());
			this->_map.push_back(std::vector<Block>());
			for (unsigned char x=0; x<width; x++) {
				this->_map[y].push_back(Block(x, y, Type::Empty));
			}
		}
		for (unsigned char x=0; x<width; x++) {
			this->_allocatedBlock.first.push_back(std::vector<unsigned char>());
		}
	};

	/**
	 * @brief	Method recive @ref Block address
	 * @param x @copydoc Block::x
	 * @param y @copydoc Block::y
	 * @throw std::invalid_argument When @p x is higher or equal @ref Board::width
	 * @throw std::invalid_argument When @p y is higher or equal @ref Board::height
	 */
	Block& Board::getBlock(unsigned char x, unsigned char y) {
		if (x >= this->width) {
			throw std::invalid_argument("X coordinate is too large! Expected value to "+std::to_string(this->width)+"!");
		}
		if (y >= this->height) {
			throw std::invalid_argument("Y coordinate is too large! Expected value to "+std::to_string(this->height)+"!");
		}
		return this->_map[y][x];
	};

	/**
	 * @brief	Parse game ID to @ref Board object
	 * @param gameID GameID (regex: '[0-9]+x[0-9]+:([0-9]*\/)+[0-9]*')
	 * @throw std::invalid_argument When @p gameID is invalid
	 * Example:
	 * @code
	 * Board newBoard = Board::parseGameID("4x4:2/1/2/3/1/1.1/3/2");
	 * @endcode
	 * @todo	Write clean code :)) and optimize if it's possible
	 */
	Board Board::parseGameID(char* gameID) {
		std::regex gameIDStructure("^([0-9]+)x([0-9]+):(([0-9]?\\.?\\/?)+)$");
		std::cmatch result;
		if (std::regex_search(gameID, result, gameIDStructure)) {
			Board board(std::stoi(result[1]), std::stoi(result[2]));
			std::string blockSessions = result[3].str();
			if (board.width+board.height-1 == std::count(blockSessions.begin(), blockSessions.end(), '/')) {
				std::replace(blockSessions.begin(), blockSessions.end(), '/', ' ');
				std::stringstream sessions(blockSessions);
				std::string accStr = "";
				for (size_t x=0; x<board.width+board.height; x++) {
					sessions >> accStr;
					std::replace(accStr.begin(), accStr.end(), '.', ' ');
					std::stringstream accNums(accStr);
					while (accNums >> accStr) {
						if (x < board.width) {
							board._allocatedBlock.first[x].push_back(std::stoi(accStr));
						} else {
							board._allocatedBlock.second[x-board.width].push_back(std::stoi(accStr));
						}
					}
				}
				return board;
			}
		}
		throw std::invalid_argument("Invalid GameID!");
	};

	/**
	 * @brief	Method return sessions of black @ref Block "blocks" in columns
	 * @param column Sequence number for sessions in column starting from left
	 * @throw	std::invalid_argument When @p column is higher or equal @ref Board::width "width" of @ref Board
	 * @return	Vector with its representing count of black @ref Block "blocks" in one session
	 */
	std::vector<unsigned char> Board::getSessionsInColumn(unsigned char column) {
		if (column >= this->width) {
			throw std::invalid_argument("Column number cannot be greater than Board width, current width: "+std::to_string(this->width)+"!");
		}
		return this->_allocatedBlock.first[column];
	};

	/**
	 * @brief	Method return sessions of black @ref Block "blocks" in rows
	 * @param row Sequence number for sessions in row starting from top
	 * @throw	std::invalid_argument When @p row is higher or equal @ref Board::height "height" of @ref Board
	 * @return	Vector with its representing count of black @ref Block "blocks" in one session
	 */
	std::vector<unsigned char> Board::getSessionsInRow(unsigned char row) {
		if (row >= this->height) {
			throw std::invalid_argument("Row number cannot be greater than Board height, current height: "+std::to_string(this->height)+"!");
		}
		return this->_allocatedBlock.second[row];
	};
}
