#ifndef SGT_UNDEAD_TYPE_CLASS
#define SGT_UNDEAD_TYPE_CLASS

#include <cstdint>

namespace sgt {
namespace undead {
    enum Type : std::uint8_t {
        Empty = 0,
        Ghost = 1,
        Vampire = 2,
        Zombie = 3,
        MirrorLeft = 4,
        MirrorRight = 5
    };
};
};

#endif