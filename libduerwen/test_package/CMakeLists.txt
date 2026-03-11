cmake_minimum_required(VERSION 3.12)
project(test_package)

include("${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
conan_basic_setup()

add_executable(example test_package.c)
target_link_libraries(example ${CONAN_LIBS})

set_target_properties(example PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
