#include "Block.h"
#include "Type.cpp"

/**
 * @author	ThePPK
 * @version	0.1
 * @file
 */

namespace sgt {
namespace pattern {
	/**
	 * @brief	Constructor for @ref Block class
	 * @param x Coordinate for block location on X axis
	 * @param y Coordinate for block location on Y axis
	 * @param blockType Type of block (default: Type::Empty)
	 */
	Block::Block(const unsigned char x, const unsigned char y, Type blockType, bool locked) : x(x), y(y) {
	
	};

	/**
	 * @brief	Method change type for block with checking possibility
	 * @param newType New type for block
	 * @throw	Exception Throw when accual or given type is unchangeable
	 */
	void Block::changeType(Type newType) {
	
	};

	/**
	 * @brief	Method give setted Type for block
	 * @return Type of block
	 */
	Type Block::getType() {
		return this->_type;
	};
}
}
