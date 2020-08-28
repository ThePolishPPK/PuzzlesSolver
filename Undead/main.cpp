#include "Board.h"
#include <assert.h>

void test() {
    game::Board board = game::Board::parseGameID((std::string) "4x4:3,3,5,bReRaRLaLb,2,4,2,0,1,3,2,3,0,2,0,3,1,2,3,2");
    assert(board.Width == 4);
    assert(board.Height == 4);

    assert(board.SeenFromTop == std::vector<int> ({2, 4, 2, 0}));
    assert(board.SeenFromBottom == std::vector<int> ({3, 0, 2, 0}));
    assert(board.SeenFromLeft == std::vector<int> ({2, 3, 2, 1}));
    assert(board.SeenFromRight == std::vector<int> ({1, 3, 2, 3}));

    assert(board.Ghosts == 3);
    assert(board.Vampires == 3);
    assert(board.Zombies == 5);

    std::vector<std::vector<game::Type>> expectedMapByType({
        std::vector<game::Type> ({game::Type::Empty, game::Type::Empty, game::Type::MirrorRight, game::Type::Empty}),
        std::vector<game::Type> ({game::Type::Empty, game::Type::Empty, game::Type::Empty, game::Type::Empty}),
        std::vector<game::Type> ({game::Type::MirrorRight, game::Type::Empty, game::Type::MirrorRight, game::Type::MirrorLeft}),
        std::vector<game::Type> ({game::Type::Empty, game::Type::MirrorLeft, game::Type::Empty, game::Type::Empty})
    });

    for (uint8_t x=0; x<board.Width; x++) {
        for (uint8_t y=0; y<board.Height; y++) {
            assert(board.getBoardBlock(x, y).BlockType == expectedMapByType[y][x]);
        }
    }
}

int main() {
    test();
    return 0;
}