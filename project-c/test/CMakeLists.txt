cmake_minimum_required(VERSION 3.12)


add_executable(read_uss_data read_uss_data.c)
# pull in common dependencies
# pull in common dependencies and adc hardware support
target_link_libraries(read_uss_data pico_stdlib hardware_adc )
# create map/bin/hex file etc.
pico_add_extra_outputs(read_uss_data)


