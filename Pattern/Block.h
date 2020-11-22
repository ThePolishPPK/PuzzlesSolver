#ifndef SGT_PATTERN_BLOCK_H
#define SGT_PATTERN_BLOCK_H

/**
 * @author ThePPK
 * @file
 */

#include "Type.cpp"

namespace sgt::pattern {
	class Block {
	public:
		Block(const unsigned char x, const unsigned char y, Type blockType=Type::Empty, bool locked=false);
		void changeType(Type newType);
		Type getType();

		const unsigned char x; //!< X coordinate of block
		const unsigned char y; //!< Y coordinate of block

	private:
		Type _type; //!< Current type of block
		bool _isStatic; //!< Define possibility of changing type
	};
}
#endif
