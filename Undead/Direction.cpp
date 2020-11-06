#ifndef SGT_UNDEAD_DIRECTION_CLASS
#define SGT_UNDEAD_DIRECTION_CLASS

#include <cstdint>

namespace sgt {
namespace undead {
	enum Direction : std::uint8_t {
		UP=0,
		RIGHT=1,
		DOWN=2,
		LEFT=3
	};
};
};

#endif
