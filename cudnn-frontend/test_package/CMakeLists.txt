cmake_minimum_required(VERSION 3.15)
project(test_package CXX)

find_package(cudnn_frontend CONFIG REQUIRED)

add_library(test_headers INTERFACE)
target_link_libraries(test_headers INTERFACE cudnn_frontend::cudnn_frontend)

if(TEST_WITH_CUDNN)
    add_executable(test_package test_package.cpp)
    target_link_libraries(test_package PRIVATE cudnn_frontend::cudnn_frontend)
    target_compile_features(test_package PRIVATE cxx_std_17)
    target_include_directories(test_package PRIVATE "${CUDNN_INCLUDE_DIR}")
else()
    message(STATUS "Skipping compile test because cuDNN headers are not available")
endif()