#include "Board.h"
#include <assert.h>

using namespace sgt::undead;

void test() {
    Board board = Board::parseGameID((std::string) "4x4:3,3,5,bReRaRLaLb,2,4,2,0,1,3,2,3,0,2,0,3,1,2,3,2");
    assert(board.Width == 4);
    assert(board.Height == 4);

    assert(board.SeenFromTop == std::vector<int> ({2, 4, 2, 0}));
    assert(board.SeenFromBottom == std::vector<int> ({3, 0, 2, 0}));
    assert(board.SeenFromLeft == std::vector<int> ({2, 3, 2, 1}));
    assert(board.SeenFromRight == std::vector<int> ({1, 3, 2, 3}));

    assert(board.Ghosts == 3);
    assert(board.Vampires == 3);
    assert(board.Zombies == 5);

    std::vector<std::vector<Type>> expectedMapByType({
        std::vector<Type> ({Type::Empty, Type::Empty, Type::MirrorRight, Type::Empty}),
        std::vector<Type> ({Type::Empty, Type::Empty, Type::Empty, Type::Empty}),
        std::vector<Type> ({Type::MirrorRight, Type::Empty, Type::MirrorRight, Type::MirrorLeft}),
        std::vector<Type> ({Type::Empty, Type::MirrorLeft, Type::Empty, Type::Empty})
    });

    for (uint8_t x=0; x<board.Width; x++) {
        for (uint8_t y=0; y<board.Height; y++) {
            assert(board.getBoardBlock(x, y).BlockType == expectedMapByType[y][x]);
        }
    }

    board.getBoardBlock(1, 1).BlockType = Type::Vampire;

    std::string out = board.exportInSolveFormat();

    auto blocks = board.getAllSeenBlock(Direction::RIGHT, 3);
    
    bool validStatus = board.isValid();
    return;
}

int main() {
    test();
    return 0;
}