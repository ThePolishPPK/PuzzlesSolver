cmake_minimum_required(VERSION 3.10)

project(Undead)

option(CMAKE_BUILD_TYPE Debug)

string(TOLOWER ${PROJECT_NAME} LIBRARY_NAME)

add_library(${LIBRARY_NAME} SHARED Block.cpp Block.h Board.cpp Board.h Direction.cpp Type.cpp Solve.cpp Solve.h)
add_executable(${PROJECT_NAME} main.cpp)

target_link_libraries(${PROJECT_NAME} ${LIBRARY_NAME})

option(MakeTests "Generate tests for project" OFF)

if (MakeTests)
	include(GoogleTest)
	add_subdirectory("test/")
endif()
