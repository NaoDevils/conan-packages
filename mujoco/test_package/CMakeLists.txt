cmake_minimum_required(VERSION 3.10.0)
project(PackageTest CXX)

find_package(MuJoCo CONFIG REQUIRED)

add_executable(example example.cpp)
target_link_libraries(example mujoco::mujoco)
target_compile_features(example PRIVATE cxx_std_17)

file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/hello.xml DESTINATION ${CMAKE_CURRENT_BINARY_DIR})