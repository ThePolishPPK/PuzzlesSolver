#include "Block.h"
#include "Type.cpp"
#include <stdexcept>
#include <exception>

/**
 * @author	ThePPK
 * @version	0.1
 * @file
 */

namespace sgt::pattern {
	/**
	 * @class Block
	 * @brief Store informations about block
	 * @details
	 * Information stored by class:
	 * 	- Coordinates of block
	 * 	- Type of block
	 */

	/**
	 * @brief	Constructor for @ref Block class
	 * @param x Coordinate for block location on X axis
	 * @param y Coordinate for block location on Y axis
	 * @param blockType @ref Type of block (default: Type::Empty)
	 * @param locked Define possibility of change block type
	 */
	Block::Block(const unsigned char x, const unsigned char y, Type blockType, bool locked) : x(x), y(y) {
		this->_type = blockType;
		this->_isStatic = locked;
	};

	/**
	 * @brief	Method change @ref Block::_type "type" for block with checking possibility
	 * @param newType New type for block
	 * @throw	std::invalid_argument Throw when Block is locked
	 */
	void Block::changeType(Type newType) {
		if (this->_isStatic) {
			throw std::exception();
		}
		this->_type = newType;
	};

	/**
	 * @brief	Method give current @ref Type for block
	 * @return Type of block
	 */
	Type Block::getType() {
		return this->_type;
	};
}
