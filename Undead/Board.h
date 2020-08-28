#ifndef UNDEAD_BOARD_H
#define UNDEAD_BOARD_H

#include <vector>
#include <string>
#include <regex>
#include "Block.cpp"

namespace game {
    class Board {
    public:
        Board(int width, int height);

        static Board parseGameID(std::basic_string<char> str);
        game::Block getBoardBlock(uint8_t x, uint8_t y);

        int Width;
        int Height;
        int Vampires;
        int Zombies;
        int Ghosts;
        std::vector<int> SeenFromTop;
        std::vector<int> SeenFromBottom;
        std::vector<int> SeenFromLeft;
        std::vector<int> SeenFromRight;

    private:
        std::vector<std::vector<game::Block>> _map;
    };
};

#endif