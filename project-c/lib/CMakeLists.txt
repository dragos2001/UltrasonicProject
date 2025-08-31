cmake_minimum_required(VERSION 3.12)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)

add_library(uss_lib 
    src/filter.c
    src/adc.c

)


target_include_directories(uss_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

# pull in common dependencies
# pull in common dependencies and adc hardware support
target_link_libraries(uss_lib
   pico_stdlib 
   hardware_adc
)




