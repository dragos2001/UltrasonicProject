# Add library from sources
add_library(uss_lib 
   ${CMAKE_CURRENT_SOURCE_DIR}/src/adc.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/filter.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/dma.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/serial.c
   ${CMAKE_CURRENT_SOURCE_DIR}/src/fft.c)
    
target_link_libraries(uss_lib pico_stdlib hardware_adc hardware_clocks hardware_dma)


# Optionally, expose headers if you have them in adc/ and filter/
target_include_directories(uss_lib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include)
