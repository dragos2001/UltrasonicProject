#Minimum C make version
cmake_minimum_required(VERSION 3.12)

#Set the target board
set(PICO_BOARD pico2)

#Import the pico sdk
include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

#Project name
project(uss_project C CXX ASM)

# Set the C/C++ version
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

# Initialize the SDK
pico_sdk_init()

# Hardware-specific examples in subdirectories:
add_subdirectory(test)
add_subdirectory(lib)
add_subdirectory(app)


