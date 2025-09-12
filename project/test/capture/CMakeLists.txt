
add_executable(capture_uss_data capture_uss_data.c)

# pull in common dependencies and adc hardware support
target_link_libraries(capture_uss_data uss_lib pico_stdlib hardware_adc hardware_clocks hardware_dma hardware_pio)

#Enable USB communication
pico_enable_stdio_usb(capture_uss_data 1)
pico_enable_stdio_uart(capture_uss_data 0)

# create map/bin/hex file etc.
pico_add_extra_outputs(capture_uss_data)


