#include "../Block.cpp"
#include "../Type.cpp"
#include <gtest/gtest.h>

using namespace sgt::undead;

const char* TypeName(Type type) {
	return (type == Type::Empty)?"Empty" 		:
	(type == Type::Ghost)? 		"Ghost"			:
	(type == Type::Vampire)?	"Vampire"		:
	(type == Type::Zombie)?		"Zombie"		:
	(type == Type::MirrorRight)?"Right Mirror"	:
	(type == Type::MirrorLeft)?	"Left Mirror"	: "Undefined Type";
}

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

TEST(BlockTest, ChangeType) {
	std::vector<Type> possibleToChangeTypes{
		Type::Empty,
		Type::Ghost,
		Type::Zombie,
		Type::Vampire
	};
	Block tempBlock(0, 0, Type::Empty);
	Block tempBlockML(0, 0, Type::MirrorLeft);
	Block tempBlockMR(0, 0, Type::MirrorRight);
	Type tempType = Type::Empty;
	std::vector<Type> changeIsPossible = {};

	for (unsigned char x=0; x<128; x++) {
		changeIsPossible.push_back(
			possibleToChangeTypes[std::rand()%possibleToChangeTypes.size()]
		);
	}
	std::random_shuffle(
		changeIsPossible.begin(),
		changeIsPossible.end()
	);

	for (auto type=changeIsPossible.begin(); type != changeIsPossible.end(); type++) {
		ASSERT_EXIT(
			{tempBlock.changeType(*type); exit(0);},
			::testing::ExitedWithCode(0),
			""
		) << "Block object doesn't accept valid type! Have assigned: <" << TypeName(tempBlock.getType()) << ">, method recived: <" << TypeName(*type) << ">!";

		ASSERT_DEATH(
			tempBlockML.changeType(*type),
			""
		) << "Block with type MirrorLeft can't be changed! Recived type: <" << TypeName(*type) << ">!";

		ASSERT_DEATH(
			tempBlockMR.changeType(*type),
			""
		) << "Block with type MirrorRight can't be changed! Recived type: <" << TypeName(*type) << ">!";
	}

	for (unsigned char x=0; x<64; x++) {
		tempType = (x%2)? Type::MirrorLeft : Type::MirrorRight;

		ASSERT_DEATH(
			tempBlock.changeType(tempType),
			""
		) << "Block object can not accept any Mirror type! Have assigned: <" << TypeName(tempBlock.getType()) << ">, method recived: <" << TypeName(tempType) << ">!";

		ASSERT_DEATH(
			tempBlockML.changeType(tempType),
			""
		) << "Block with type MirrorLeft can't be changed! Recived type: <" << TypeName(tempType) << ">!";

		ASSERT_DEATH(
			tempBlockMR.changeType(tempType),
			""
		) << "Block with type MirrorRight can't be changed! Recived type: <" << TypeName(tempType) << ">!";
	}
}