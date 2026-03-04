cmake_minimum_required(VERSION 3.1.0)
project(cmake_wrapper)

# Conan toolchain settings are injected via CMAKE_TOOLCHAIN_FILE (conan_toolchain.cmake).
# No conanbuildinfo.cmake needed with the new Conan v2 / CMakeToolchain API.

add_subdirectory("source_subfolder")
