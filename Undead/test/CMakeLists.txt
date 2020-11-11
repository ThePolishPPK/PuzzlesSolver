cmake_minimum_required(VERSION 3.10)

project(UndeadTest)

find_library(undead Required)
find_library(gtest PATHS )

set(TEST_LIST BoardTest.cpp BlockTest.cpp SolveTest.cpp)

link_directories($ENV{HOME}/.local/lib/gtest/)

set(CMAKE_LIBRARY_PATH $ENV{HOME}/.local/lib/gtest ${CMAKE_LIBRARY_PATH})

add_executable(${PROJECT_NAME} main.cpp ${TEST_LIST})

target_link_libraries(${PROJECT_NAME} undead gtest gtest_main)
