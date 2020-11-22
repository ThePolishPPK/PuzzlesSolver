#include "Board.h"
#include "Block.h"
#include <stdexcept>

/**
 * @author ThePPK
 * @file
 */

namespace sgt::pattern {
	/**
	 * @brief	Constructor for @ref Board class
	 * @param width @copydoc Board::width
	 * @param height @copydoc Board::height
	 * @throw	std::invalid_argument When @p width or @p height equal zero
	 * @todo	Make argument validator and make map
	 */
	Board::Board(unsigned char width, unsigned char height) : width(width), height(height) {
	
	};

	/**
	 * @brief	Method recive @ref Block address
	 * @param x @copydoc Block::x
	 * @param y @copydoc Block::y
	 * @throw std::invalid_argument When @p x is higher or equal @ref Board::width
	 * @throw std::invalid_argument When @p y is higher or equal @ref Board::height
	 * @todo Make method
	 */
	Block& Board::getBlock(unsigned char x, unsigned char y) {
	
	};

	/**
	 * @brief	Parse game ID to board object
	 * @param gameID GameID (regex: '[0-9]+x[0-9]+:([0-9]*\/)+[0-9]*')
	 * @throw std::invalid_argument When @p gameID is invalid
	 * Example:
	 * @code
	 * Board newBoard = Board::parseGameID("4x4:2/1/2/3/1/1.1/3/2");
	 * @endcode
	 * @todo	Make parser
	 */
	Board Board::parseGameID(char* gameID) {
	
	};

	/**
	 * @brief	Method return sessions of black blocks in columns
	 * @param column Sequence number for sessions in column starting from left
	 * @throw	std::invalid_argument When @p column is higher or equal width of Board
	 * @return	Vector with its representing count of black blocks in one session
	 * @todo	Make method
	 */
	std::vector<unsigned char> Board::getSessionsInColumn(unsigned char column) {
	
	};

	/**
	 * @brief	Method return sessions of black blocks in rows
	 * @param row Sequence number for sessions in row starting from top
	 * @throw	std::invalid_argument When @p row is higher or equal height of Board
	 * @return	Vector with its representing count of black blocks in one session
	 * @todo	Make method
	 */
	std::vector<unsigned char> Board::getSessionsInRow(unsigned char row) {
	
	};
}
