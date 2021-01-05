#ifndef SGT_PATTERN_BOARD_H
#define SGT_PATTERN_BOARD_H

#include "Block.h"
#include <vector>
#include <string>
#include <istream>

namespace sgt::pattern {
	class Board {
	public:
		Board(unsigned char width, unsigned char height);
		static Board parseGameID(char* gameID);
		static Board parseSave(std::istream& saveStream);
		static Board parseSave(std::string& save);
		Block& getBlock(unsigned char x, unsigned char y);
		std::vector<unsigned char> getSessionsInColumn(unsigned char column);
		std::vector<unsigned char> getSessionsInRow(unsigned char row);
		std::string exportSave();
		std::string exportGameID();
		
		const unsigned char width; //!< Width of board / Count of blocks in row
		const unsigned char height; //!< Height of board / Count of blocks in column

	private:
		std::vector<
			std::vector<Block>
		> _map; //!< 2D vector with Blocks
		std::pair<
			std::vector<std::vector<unsigned char>>,// TOP
			std::vector<std::vector<unsigned char>>	// LEFT
		> _allocatedBlock; //!< Contain informations about length sessions of Type::Black Blocks
	};
}

#endif
