#ifndef SGT_UNDEAD_BLOCK_CLASS
#define SGT_UNDEAD_BLOCK_CLASS

#include "Type.cpp"
#include <assert.h>

namespace sgt {
namespace undead {
    class Block {
    public:
        Block(int x, int y, Type type) {
            assert(x >= 0);
            assert(y >= 0);

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