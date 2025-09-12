
add_executable(read_uss_data read_uss_data.c)

# pull in common dependencies and adc hardware support
target_link_libraries(read_uss_data uss_lib pico_stdlib hardware_adc hardware_clocks )


#Enable USB communication
pico_enable_stdio_usb(read_uss_data 1)
pico_enable_stdio_uart(read_uss_data 0)


# create map/bin/hex file etc.
pico_add_extra_outputs(read_uss_data)


