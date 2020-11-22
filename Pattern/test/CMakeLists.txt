project(PatternTest)

option(CMAKE_BUILD_TYPE Debug)
link_directories($ENV{HOME}/.local/lib/gtest/)

set(TEST_LIST
	main.cpp
	BlockTest.cpp
	BoardTest.cpp
)

add_executable(${PROJECT_NAME} main.cpp ${TEST_LIST})

target_link_libraries(${PROJECT_NAME} Pattern gtest gtest_main)
