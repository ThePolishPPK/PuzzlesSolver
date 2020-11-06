#include "Board.h"
#include "Type.cpp"
#include <cassert>
#include <stdexcept>

namespace sgt {
namespace undead {
	bool Board::isValid() {
		std::vector<std::pair<Direction, std::vector<int>*>> directions = {
			std::make_pair(Direction::UP, &this->SeenFromTop),
			std::make_pair(Direction::DOWN, &this->SeenFromBottom),
			std::make_pair(Direction::LEFT, &this->SeenFromLeft),
			std::make_pair(Direction::RIGHT, &this->SeenFromRight)
		};
		uint16_t seenMonsters;
		for (uint8_t e=0; e<directions.size(); e++) {
			for (uint16_t x=0; x<directions[e].second->size(); x++) {
				seenMonsters = 0;
				auto seenBlocks = this->getAllSeenBlocks(directions[e].first, x);
				for (auto block=seenBlocks.begin(); block != seenBlocks.end(); block++){
					if (
						(*block->first).BlockType == Type::Zombie ||
						((*block->first).BlockType == Type::Vampire && block->second) ||
						((*block->first).BlockType == Type::Ghost && block->second == false)
					) {
						seenMonsters++;
					}
				}
				if (seenMonsters > (*directions[e].second)[x]) {
					return false;
				}
			}
			return true;
		}
		return true;
	}

	std::vector<std::pair<Block *, bool>> Board::getAllSeenBlocks(Direction direction, const uint& axisLocation) {
		int8_t xIncrement(0);
		int8_t yIncrement(0);
		uint16_t x(0);
		uint16_t y(0);
		bool beforeMirror = true;
		std::vector<std::pair<Block *, bool>> result;
		Block* tempBlock;

		switch (direction) {
			case Direction::LEFT:
				xIncrement = 1;
				break;
			case Direction::RIGHT:
				xIncrement = -1;
				x = this->Width - 1;
				break;
			case Direction::UP:
				yIncrement = 1;
				break;
			case Direction::DOWN:
				yIncrement = -1;
				y = this->Height - 1;
		}

		if (xIncrement != 0) {
			y = axisLocation;
		} else x = axisLocation;

		while  (x >= 0 && x < this->Width &&
				y >= 0 && y < this->Height) {
			tempBlock = &this->getBlock(x, y);
			switch (tempBlock->BlockType) {
				case Type::MirrorLeft:
					if (yIncrement == 0) {
						yIncrement = xIncrement;
						xIncrement = 0;
					} else {
						xIncrement = yIncrement;
						yIncrement = 0;
					}
					beforeMirror = false;
					break;
				case Type::MirrorRight:
					if (yIncrement == 0) {
						yIncrement = -xIncrement;
						xIncrement = 0;
					} else {
						xIncrement = -yIncrement;
						yIncrement = 0;
					}
					beforeMirror = false;
					break;
				default:
					result.push_back(std::make_pair(tempBlock, beforeMirror));
			}
			x += xIncrement;
			y += yIncrement;
		}
		return result;
	}

	std::string Board::exportInSolveFormat() {
		std::string output;
		unsigned int offset = 0;
		for (unsigned int y=0; y<this->Height; y++) {
			for (unsigned int x=0; x<this->Width; x++) {
				char letter = 0;
				switch (this->_map[y][x].BlockType) {
					case Type::Ghost:
						letter = 'G';
						break;
					case Type::Vampire:
						letter = 'V';
						break;
					case Type::Zombie:
						letter = 'Z';
						break;
					case Type::Empty:
						letter = ' ';
						break;
					default:
						break;
				}
				if (letter != 0) {
					for (char c: letter + std::to_string(offset) + ";") {
						output.push_back(c);
					}
					offset++;
				}
			}
		}
		if (output.length() == 0) {
			return std::string("");
		}
		return output.substr(0, output.length()-1);
	}

	Block& Board::getBlock(uint8_t x, uint8_t y) {
		assert(x >= 0 and x < this->Width);
		assert(y >= 0 and y < this->Height);

		return this->_map[y][x];
	}

	Board Board::parseGameID(const std::string& gameID) {
		bool previousSegmentsAreOK = true;

		std::smatch localStringMatch;
		Board board(1,1);

		if (std::regex_match(gameID, localStringMatch, std::regex("^([0-9]+)x([0-9]+):.+"))) {
			board = Board((int) (*localStringMatch[1].first.base() - '0'), (int) (*localStringMatch[2].first - '0'));
		} else previousSegmentsAreOK = false;


		if (previousSegmentsAreOK and std::regex_match(gameID, localStringMatch, std::regex(".+:([0-9]+),([0-9]+),([0-9]+),.+"))) {
			board.Ghosts = (*localStringMatch[1].first - '0');
			board.Vampires = (*localStringMatch[2].first - '0');
			board.Zombies = (*localStringMatch[3].first - '0');
		} else previousSegmentsAreOK = false;


		if (previousSegmentsAreOK and
			std::regex_search(
					gameID,
					localStringMatch,
					std::regex(",(([0-9]+,?)+)$"),
					std::regex_constants::format_sed
		)) {
			std::string seenMonstersLine (localStringMatch[0].first+1, localStringMatch[0].second);
			std::vector<uint8_t> seenMonsters;
			uint offset;

			for (uint x=0; x<seenMonstersLine.size(); x++) {
				offset=seenMonstersLine.find(',', x);
				seenMonsters.push_back(
					std::stoi((std::string) seenMonstersLine.substr(x, offset))
				);
				if (offset < seenMonstersLine.size()) x = offset;
			}

			assert(seenMonsters.size() == (board.Width+board.Height)*2);

			board.SeenFromTop = std::vector<int> (seenMonsters.begin(), seenMonsters.begin()+board.Width);
			board.SeenFromRight = std::vector<int> (seenMonsters.begin()+board.Width, seenMonsters.begin()+board.Width+board.Height);
			board.SeenFromBottom = std::vector<int> (seenMonsters.rbegin()+board.Height, seenMonsters.rbegin()+board.Height+board.Width);
			board.SeenFromLeft = std::vector<int> (seenMonsters.rbegin(), seenMonsters.rbegin()+board.Height);
		} else previousSegmentsAreOK = false;

		if (previousSegmentsAreOK and
			std::regex_search(gameID, localStringMatch, std::regex(",([a-z]?(L|R))+[a-z]?,"), std::regex_constants::format_sed)) {
			std::string mirrorsData (localStringMatch[0].first+1, localStringMatch[0].second-1);

			unsigned int offset = 0;
			for (char chr: mirrorsData) {
				if (chr == 'R') {
					board._map[offset / board.Width][offset % board.Height].BlockType = Type::MirrorRight;
				} else if (chr == 'L') {
					board._map[offset / board.Width][offset % board.Height].BlockType = Type::MirrorLeft;
				} else {
					offset += (int) chr - 97;
				}
				offset += 1;
			}
		} else previousSegmentsAreOK = false;

		if (previousSegmentsAreOK) {
			return board;
		}

		throw std::invalid_argument("Parameter {gameID} has invalid structure! \n Expected structure (RegExp): [0-9]+x[0-9]+:([0-9]\\,?)+\\,([a-z]?(L|R)\\,)+([0-9]+\\,)+\nExample: 3x3:2,2,2,bRcRaR,2,2,0,2,2,0,0,2,2,1,2,2");
	}

	Board::Board(char width, char height) {
		if (width <= 0 || height <= 0 || width > 12 || height > 12) {
			throw std::invalid_argument("Width must be greater than 0!");
		}

		this->Height = height;
		this->Width = width;
		this->Ghosts = 0;
		this->Vampires = 0;
		this->Zombies = 0;
		for (unsigned y=0; y<height; y++) {
			this->_map.emplace_back();
			for (unsigned x=0; x<width; x++) {
				this->_map[y].push_back(Block((int) x, (int) y, (Type) Type::Empty));
			}
		}
	}
};
};
