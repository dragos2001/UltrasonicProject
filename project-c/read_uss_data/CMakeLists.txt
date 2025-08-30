cmake_minimum_required(VERSION 3.12)

include($ENV{PICO_SDK_PATH}/external/pico_sdk_import.cmake)

project(read_uss_data C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

add_executable(read_uss_data
    read_uss_data.c
    )

# pull in common dependencies
# pull in common dependencies and adc hardware support
target_link_libraries(read_uss_data pico_stdlib hardware_adc )


if (PICO_CYW43_SUPPORTED)
    target_link_libraries(read_uss_data  pico_cyw43_arch_none)
endif()

pico_sdk_init()
# create map/bin/hex file etc.
pico_add_extra_outputs(read_uss_data)


