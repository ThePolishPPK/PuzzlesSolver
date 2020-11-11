#ifndef SGT_UNDEAD_BLOCK_CLASS
#define SGT_UNDEAD_BLOCK_CLASS

#include "Type.cpp"
#include <assert.h>

namespace sgt {
namespace undead {
	class Block {
	public:
		Block(short x, short y, Type type) : x(x), y(y), BlockType(type) {
			assert(x >= 0 and x < 128);
			assert(y >= 0 and y < 128);
		};

		void changeType(Type type) {
			assert(type != Type::MirrorLeft and this->BlockType != Type::MirrorLeft);
			assert(type != Type::MirrorRight and this->BlockType != Type::MirrorRight);

			this->BlockType = type;
		};

		Type getType() {
			return this->BlockType;
		};

	public:
		const unsigned char x;
		const unsigned char y;
		Type BlockType;
	};
};
};
#endif
