#ifndef BLOCK_CLASS
#define BLOCK_CLASS

#include "Type.cpp"
#include <assert.h>

namespace game {
    class Block {
    public:
        Block(int x, int y, game::Type *type) {
            assert(x >= 0);
            assert(y >= 0);

            this->x = x;
            this->y = y;
            this->BlockType = type;
        };

    public:
        int x;
        int y;
        game::Type* BlockType;
    };

};

#endif