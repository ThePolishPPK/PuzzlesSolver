#ifndef SGT_UNDEAD_BOARD_HEADER
#define SGT_UNDEAD_BOARD_HEADER

#include <vector>
#include <string>
#include <regex>
#include "Block.cpp"
#include "Direction.cpp"

namespace sgt {
namespace undead {
	class Board {
	public:
		Board(char width, char height);

		static Board parseGameID(const std::basic_string<char>& str);
		Block& getBlock(uint8_t x, uint8_t y);
		std::string exportInSolveFormat();
		std::vector<std::pair<Block *, bool>> getAllSeenBlocks(Direction direction, const uint& axisLocation = 0);
		bool isValid();

		unsigned int Width;
		unsigned int Height;
		unsigned int Vampires;
		unsigned int Zombies;
		unsigned int Ghosts;
		std::vector<int> SeenFromTop;
		std::vector<int> SeenFromBottom;
		std::vector<int> SeenFromLeft;
		std::vector<int> SeenFromRight;

	private:
		std::vector<std::vector<Block>> _map;
	};
};
};

#endif
