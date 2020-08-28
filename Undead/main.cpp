#include "Board.h"
#include <assert.h>

void test() {
    Board::parseGameID(
        //(std::string) "4x4:3,3,5,bReRaRLaLb,2,4,2,0,1,3,2,3,0,2,0,3,1,2,3,2"
        (std::string) "4x4:3,3,5,bReRaRLaLb,2,4,2,0,1,3,2,3,0,2,0,3,1,2,3,2"
    );
}

int main() {
    test();
    return 0;
}