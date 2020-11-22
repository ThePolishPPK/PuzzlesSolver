#include "Block.h"
#include "Type.cpp"

/**
 * @author	ThePPK
 * @version	0.1
 * @file
 */

namespace sgt::pattern {
	/**
	 * @class Block
	 * @brief Store informations about block
	 * Information stored by class:
	 * 	- Coordinates of block
	 * 	- Type of block
	 */

	/**
	 * @brief	Constructor for @ref Block class
	 * @param x Coordinate for block location on X axis
	 * @param y Coordinate for block location on Y axis
	 * @param blockType Type of block (default: Type::Empty)
	 * @todo	Make varuables assign
	 */
	Block::Block(const unsigned char x, const unsigned char y, Type blockType, bool locked) : x(x), y(y) {
	
	};

	/**
	 * @brief	Method change type for block with checking possibility
	 * @param newType New type for block
	 * @throw	Exception Throw when accual or given type is unchangeable
	 * @todo	Make method
	 */
	void Block::changeType(Type newType) {
	
	};

	/**
	 * @brief	Method give current Type for block
	 * @return Type of block
	 */
	Type Block::getType() {
		return this->_type;
	};
}
