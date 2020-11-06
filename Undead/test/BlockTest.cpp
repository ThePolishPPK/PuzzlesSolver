#include "../Block.cpp"
#include "../Type.cpp"
#include <gtest/gtest.h>

using namespace sgt::undead;

TEST(BlockTest, Constructor) {
	unsigned char x, y, z, t;
	Type types[] = {Type::Empty, Type::Ghost, Type::MirrorLeft, Type::MirrorRight, Type::Vampire, Type::Zombie};
	Block tempBlock(0, 0, Type::Empty);

	for (z=0; z<128; z++) {
		x = std::rand() % 128;
		y = std::rand() % 128;
		t = std::rand() % 6;

		tempBlock = Block(x, y, types[t]);

		ASSERT_EQ(tempBlock.x, x) << "X coordinate is invalid!";
		ASSERT_EQ(tempBlock.y, y) << "Y coordinate is invalid!";
		ASSERT_EQ(tempBlock.BlockType, types[t]) << "Type value is invalid!";
	}

	std::vector<std::tuple<short, short, Type>> blocksData = {
		{-3, 0, Type::MirrorRight},
		{3, 129, Type::Empty},
		{2, 128, Type::Ghost},
		{3, -129, Type::Zombie},
		{-135, 9, Type::MirrorLeft},
		{129, 2, Type::Vampire},
		{128, 1, Type::Ghost},
		{135, 169, Type::MirrorLeft},
		{128, 128, Type::Ghost}
	};

	for (auto i = blocksData.begin(); i != blocksData.end(); i++) {
		ASSERT_DEATH(Block(
			std::get<0>(*i),
			std::get<1>(*i),
			std::get<2>(*i)
		), "") << "Coordinates must be in range from 0 to 128.";
	}

}
