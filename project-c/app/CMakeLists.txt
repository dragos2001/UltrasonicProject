cmake_minimum_required(VERSION 3.12)

add_executable(main src/main.c)

# pull in common dependencies
# pull in common dependencies and adc hardware support
target_link_libraries(main uss_lib pico_stdlib hardware_adc )

#Enable USB communication
pico_enable_stdio_usb(main 1)
pico_enable_stdio_uart(main 0)

# create map/bin/hex file etc.
pico_add_extra_outputs(main)


