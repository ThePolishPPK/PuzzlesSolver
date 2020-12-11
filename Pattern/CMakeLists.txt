cmake_minimum_required(VERSION 3.10)
project(Pattern)

option(Tests "Generate tests for project" OFF)
option(Debug "Make in debug mode" OFF)

if (Debug)
	option(CMAKE_BUILD_TYPE Debug)
	add_compile_options(-g)
endif()

add_library(${PROJECT_NAME} SHARED
Type.cpp
Block.h Block.cpp
Board.h Board.cpp
Solve.h Solve.cpp
)

if (Tests)
	add_subdirectory("test/")
endif()
