cmake_minimum_required(VERSION 3.15)
project(test_package C)

find_package(duerwen_wakeup_doa CONFIG REQUIRED)

if(NOT TARGET duerwen_wakeup_doa::duerwen_wakeup_doa)
    message(STATUS "Skipping test_package: no duerwen_wakeup_doa target on this platform")
    return()
endif()

add_executable(example src/test_package.c)
target_link_libraries(example PRIVATE duerwen_wakeup_doa::duerwen_wakeup_doa)