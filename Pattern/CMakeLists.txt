cmake_minimum_required(VERSION 3.10)
project(Pattern)

option(Tests "Generate tests for project" OFF)
option(Debug "Make in debug mode" OFF)

if (Debug)
	option(CMAKE_BUILD_TYPE Debug)
endif()

add_library(${PROJECT_NAME} SHARED Block.h Block.cpp Type.cpp)

if (Tests)
	add_subdirectory("test/")
endif()
