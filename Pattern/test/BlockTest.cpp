#include <gtest/gtest.h>
#include "../Block.h"
#include "../Type.cpp"
#include <tuple>
#include <vector>

using namespace sgt::pattern;

TEST(BlockTest, Constructor) {
	std::vector<std::tuple<
		unsigned char,
		unsigned char,
		Type
	>> testData = {
		{3, 7, Type::Black},
		{11, 3, Type::White},
		{8, 6, Type::Empty},
		{3, 0, Type::Empty},
		{0, 5, Type::White},
		{0, 0, Type::Black}
	};
	for (auto data=testData.begin(); data != testData.end(); data++) {
		Block tempBlock(
			std::get<0>(*data),
			std::get<1>(*data),
			std::get<2>(*data)
		);
		ASSERT_EQ(tempBlock.x, std::get<0>(*data));
		ASSERT_EQ(tempBlock.y, std::get<1>(*data));
		ASSERT_EQ(tempBlock.getType(), std::get<2>(*data));
	}

	Block tempBlock(4, 1);
	ASSERT_EQ(tempBlock.x, 4);
	ASSERT_EQ(tempBlock.y, 1);
	ASSERT_EQ(tempBlock.getType(), Type::Empty);
}

TEST(BlockTest, changeType) {
	Block changableBlock(3, 7);
	Block unchangeableBlock(4, 2,Type::Empty, true);
	ASSERT_NO_THROW({changableBlock.changeType(Type::Black);}) << "Block was been declared as unlocked and must be changeable!";
	ASSERT_EQ(changableBlock.getType(), Type::Black) << "Type wasn't been changed!";
	ASSERT_ANY_THROW(unchangeableBlock.changeType(Type::White);) << "Block was been declared as locked and mustn't be changeable!";
}
