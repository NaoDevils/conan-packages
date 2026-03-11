cmake_minimum_required(VERSION 3.15)
project(test_package)

find_package(duerwen_wakeup_DOA REQUIRED)

add_executable(example src/test_package.c)
target_link_libraries(example duerwen_wakeup_DOA::duerwen_wakeup_DOA)

set_target_properties(example PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin"
)
