#include "../Board.h"
#include <math.h>
#include <gtest/gtest.h>
#include <stdexcept>

using namespace sgt::undead;


TEST(BoardTest, Constructor) {
    Board obj(10, 5);

    // Defined board sizes
    ASSERT_EQ(5, obj.Height) << "Height must be exactly equal second parameter in constructor!";
    ASSERT_EQ(10, obj.Width) << "Width must be exactly equal first parameter in constructor!";

    // Default values
    EXPECT_EQ(0, obj.Ghosts) << "Ghosts count by default should be 0!";
    EXPECT_EQ(0, obj.Vampires) << "Vampires count by default should be 0!";
    EXPECT_EQ(0, obj.Zombies) << "Zombies count by default should be 0!";

    bool throwExcept = false;
    
    // Check minimum board size parameters
    int args[2];
    for (unsigned char x=0; x<16; x++) {
        throwExcept = false;
        args[x%2] = std::rand() % 12;
        args[(x+1)%2] = (x%5)? 0 : -(std::rand()%12);
        
        try {
            Board(args[0], args[1]);
        } catch (const std::invalid_argument& err) {
            throwExcept = true;
        }
        ASSERT_TRUE(throwExcept) << "Constructor doesn't throw exception of Width or/and Height lower than 1! Tested for width=" << args[0] << " and height=" << args[1] << "!";
    }
    
    // Check maximum board size parameters
    for (unsigned char x=0; x<16; x++) {
        throwExcept = false;
        args[0] = (std::rand() % 12)+((x%2)? 13 : 1);
        args[1] = (std::rand() % 12)+(((x+1)%2)? 13 : 1);
        
        if (std::rand() % 5 == 0) {
            args[(x+1)%2] += 13;
        }
        
        try {
            Board(args[0], args[1]);
        } catch (const std::invalid_argument& err) {
            throwExcept = true;
        }
        ASSERT_TRUE(throwExcept) << "Maximum Board size that is 12 width and 12 height! Tested for width=" << args[0] << " and height=" << args[1] << "!";


    }
}

TEST(BoardTest, getBoardBlock) {
    // Test created map
    unsigned char x,y;
    Board test(
        (std::rand() % 4) + 8,
        (std::rand() % 4) + 8
    );
    Block* tempBlock;
    
    for (x=0; x<test.Width; x++) {
        for (y=0; y<test.Height; y++) {
            tempBlock = &test.getBoardBlock(x, y);
            ASSERT_EQ(tempBlock->x, x);
            ASSERT_EQ(tempBlock->y, y);
            ASSERT_EQ(tempBlock->BlockType, Type::Empty);
        }
    }
    
    std::vector<std::pair<char, char>> parameters = {
        {std::rand()%test.Width, test.Height},
        {test.Width, std::rand()%test.Height},
        {-1, 4},
        {-87, 2},
        {3, 43},
        {7, -76}
    };
    
    for (auto i = parameters.begin(); i != parameters.end(); i++) {
        ASSERT_DEATH(test.getBoardBlock(i->first, i->second), "");
    }
}