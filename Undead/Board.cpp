#include "Board.h"
#include "Type.cpp"
#include <assert.h>

game::Block game::Board::getBoardBlock(uint8_t x, uint8_t y) {
    assert(x >= 0 and x < this->Width);
    assert(y >= 0 and y < this->Height);

    return this->_map[y][x];
}

game::Board game::Board::parseGameID(std::string gameID) {
    bool previusSegmentsAreOK = true;
    std::vector<std::vector<int>> seenMonsters(4);

    std::smatch localStringMatch;
    game::Board board(1,1);

    if (previusSegmentsAreOK and std::regex_match(gameID, localStringMatch, std::regex("^([0-9]+)x([0-9]+):.+"))) {
        board = Board((int) (*localStringMatch[1].first.base() - '0'), (int) (*localStringMatch[2].first - '0'));
    } else previusSegmentsAreOK = false;


    if (previusSegmentsAreOK and std::regex_match(gameID, localStringMatch, std::regex(".+:([0-9]+),([0-9]+),([0-9]+),.+"))) {
        board.Ghosts = (*localStringMatch[1].first - '0');
        board.Vampires = (*localStringMatch[2].first - '0');
        board.Zombies = (*localStringMatch[3].first - '0');
    } else previusSegmentsAreOK = false;


    if (previusSegmentsAreOK and
        std::regex_search(
                gameID,
                localStringMatch,
                std::regex(",(([0-9]+,?)+)$"),
                std::regex_constants::format_sed
    )) {
        std::string seenMonstersLine (localStringMatch[0].first+1, localStringMatch[0].second);
        std::vector<uint8_t> seenMonsters;
        uint offset=0;

        for (uint x=0; x<seenMonstersLine.size(); x++) {
            offset=seenMonstersLine.find(",", x);
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
    } else previusSegmentsAreOK = false;

    if (previusSegmentsAreOK and
        std::regex_search(gameID, localStringMatch, std::regex(",([a-z]?(L|R))+[a-z]?,"), std::regex_constants::format_sed)) {
        std::string mirrorsData (localStringMatch[0].first+1, localStringMatch[0].second-1);

        unsigned int offset = 0;
        for (char chr: mirrorsData) {
            if (chr == (char &) "R") {
                board._map[offset / board.Width][offset % board.Height].BlockType = game::Type::MirrorRight;
            } else if (chr == (char &) "L") {
                board._map[offset / board.Width][offset % board.Height].BlockType = game::Type::MirrorLeft;
            } else {
                offset += (int) chr - 97;
            }
            offset += 1;
        }
    } else previusSegmentsAreOK = false;

    if (previusSegmentsAreOK) {
        return board;
    }

    throw std::invalid_argument("Parameter {gameID} has invalid structure! \n Expected structure (RegExp): [0-9]+x[0-9]+:([0-9]\\,?)+\\,([a-z]?(L|R)\\,)+([0-9]+\\,)+\nExample: 3x3:2,2,2,bRcRaR,2,2,0,2,2,0,0,2,2,1,2,2");
}

game::Board::Board(int width, int height) {
    assert(width > 0);
    assert(height > 0);
    this->Height = height;
    this->Width = width;
    for (unsigned y=0; y<height; y++) {
        this->_map.emplace_back();
        for (unsigned x=0; x<width; x++) {
            this->_map[y].push_back(game::Block((int) x, (int) y, game::Type::Empty));
        }
    }
}
