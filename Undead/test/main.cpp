#include <gtest/gtest.h>

int main(int argc,char **argv)
{
	testing::InitGoogleTest(&argc,argv);
	std::srand(std::time(0));
	return RUN_ALL_TESTS();

}
