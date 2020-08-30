#ifndef TYPE_CLASS
#define TYPE_CLASS

#include <cstdint>

namespace game {
    enum Type : std::uint8_t {
        Empty = 0,
        Ghost = 1,
        Vampire = 2,
        Zombie = 3,
        MirrorLeft = 4,
        MirrorRight = 5
    };
};

#endif