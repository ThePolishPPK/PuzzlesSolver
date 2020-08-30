#ifndef DIRECTION_CLASS
#define DIRECTION_CLASS

#include <cstdint>

namespace game {
    enum Direction : std::uint8_t {
        UP=0,
        RIGHT=1,
        DOWN=2,
        LEFT=3
    };
};

#endif