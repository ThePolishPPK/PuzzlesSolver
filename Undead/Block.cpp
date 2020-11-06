#ifndef SGT_UNDEAD_BLOCK_CLASS
#define SGT_UNDEAD_BLOCK_CLASS

#include "Type.cpp"
#include <assert.h>

namespace sgt {
namespace undead {
	class Block {
	public:
		Block(short x, short y, Type type) {
			assert(x >= 0 and x < 128);
			assert(y >= 0 and y < 128);

			this->x = x;
			this->y = y;
			this->BlockType = type;
		};

	public:
		int x;
		int y;
		Type BlockType;
	};
};
};
#endif
