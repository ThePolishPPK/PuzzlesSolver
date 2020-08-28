cmake_minimum_required(VERSION 3.17)
project(Undead)

set(CMAKE_CXX_STANDARD 20)

add_executable(Undead Board.cpp Block.cpp Block.cpp Board.h Type.cpp main.cpp)