#include "Board.h"
#include "Type.cpp"
#include <cassert>

std::vector<game::Block*> game::Board::getAllSeenBlock(game::Direction direction, const uint& axisLocation) {
    int8_t xIncrement(0);
    int8_t yIncrement(0);
    uint16_t x(0);
    uint16_t y(0);
    std::vector<game::Block*> result;
    game::Block* tempBlock;

    switch (direction) {
        case game::Direction::LEFT:
            xIncrement = 1;
            break;
        case game::Direction::RIGHT:
            xIncrement = -1;
            x = this->Width - 1;
            break;
        case game::Direction::DOWN:
            yIncrement = 1;
            break;
        case game::Direction::UP:
            yIncrement = -1;
            y = this->Height - 1;
    }

    if (xIncrement != 0) {
        y = axisLocation;
    } else x = axisLocation;

    while  (x >= 0 && x < this->Width &&
            y >= 0 && y < this->Height) {
        tempBlock = &this->getBoardBlock(x, y);
        switch ((game::Type &) tempBlock->BlockType) {
            case game::Type::MirrorLeft:
                if (yIncrement == 0) {
                    yIncrement = xIncrement;
                    xIncrement = 0;
                } else {
                    xIncrement = yIncrement;
                    yIncrement = 0;
                }
                break;
            case game::Type::MirrorRight:
                if (yIncrement == 0) {
                    yIncrement = -xIncrement;
                    xIncrement = 0;
                } else {
                    xIncrement = -yIncrement;
                    yIncrement = 0;
                }
                break;
            default:
                result.push_back(tempBlock);
        }
        x += xIncrement;
        y += yIncrement;
    }
    return result;
}

std::string game::Board::exportInSolveFormat() {
    std::string output;
    unsigned int offset = 0;
    for (unsigned int y=0; y<this->Height; y++) {
        for (unsigned int x=0; x<this->Width; x++) {
            char letter = 0;
            switch ((game::Type &) this->_map[y][x].BlockType) {
                case game::Type::Ghost:
                    letter = 'G';
                    break;
                case game::Type::Vampire:
                    letter = 'V';
                    break;
                case game::Type::Zombie:
                    letter = 'Z';
                    break;
                case game::Type::Empty:
                    letter = ' ';
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

game::Block& game::Board::getBoardBlock(uint8_t x, uint8_t y) {
    assert(x >= 0 and x < this->Width);
    assert(y >= 0 and y < this->Height);

    return this->_map[y][x];
}

game::Board game::Board::parseGameID(const std::string& gameID) {
    bool previousSegmentsAreOK = true;

    std::smatch localStringMatch;
    game::Board board(1,1);

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
                board._map[offset / board.Width][offset % board.Height].BlockType = (game::Type *) game::Type::MirrorRight;
            } else if (chr == 'L') {
                board._map[offset / board.Width][offset % board.Height].BlockType = (game::Type *) game::Type::MirrorLeft;
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

game::Board::Board(int width, int height) {
    assert(width > 0);
    assert(height > 0);
    this->Height = height;
    this->Width = width;
    this->Ghosts = 0;
    this->Vampires = 0;
    this->Zombies = 0;
    for (unsigned y=0; y<height; y++) {
        this->_map.emplace_back();
        for (unsigned x=0; x<width; x++) {
            this->_map[y].push_back(game::Block((int) x, (int) y, (game::Type *) game::Type::Empty));
        }
    }
}
