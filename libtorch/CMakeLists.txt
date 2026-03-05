cmake_minimum_required(VERSION 3.12)
project(cmake_wrapper)

# Conan v2 / CMakeToolchain: toolchain is injected via CMAKE_TOOLCHAIN_FILE.
# Dependencies are provided via CMakeDeps-generated config files (find_package).
# No conanbuildinfo.cmake needed.

#-----------------------------
# Workaround for github action
# see https://github.com/actions/setup-python/issues/121#issuecomment-777748504
if (POLICY CMP0094)
    cmake_policy(SET CMP0094 NEW)
endif ()
if (NOT DEFINED Python_FIND_REGISTRY)
    set(Python_FIND_REGISTRY "LAST")
endif ()
if (NOT DEFINED Python_FIND_FRAMEWORK)
    set(Python_FIND_FRAMEWORK "LAST")
endif ()
#-----------------------------

find_package(Python 3.8.0 REQUIRED)
set(PYTHON_EXECUTABLE ${Python_EXECUTABLE})

find_package(Eigen3 REQUIRED CONFIG)
set(EIGEN3_FOUND 1)
set(EIGEN3_INCLUDE_DIR ${Eigen3_INCLUDE_DIR})

find_package(cpuinfo REQUIRED CONFIG)
add_library(cpuinfo INTERFACE IMPORTED)
set_property(TARGET cpuinfo PROPERTY INTERFACE_LINK_LIBRARIES cpuinfo::cpuinfo)
add_library(clog INTERFACE IMPORTED)
set_property(TARGET clog PROPERTY INTERFACE_LINK_LIBRARIES cpuinfo::cpuinfo)

if(USE_PYTORCH_QNNPACK)
    find_package(fxdiv REQUIRED CONFIG)
    add_library(fxdiv INTERFACE IMPORTED)
    set_property(TARGET fxdiv PROPERTY INTERFACE_LINK_LIBRARIES fxdiv::fxdiv)

    find_package(psimd REQUIRED CONFIG)
    add_library(psimd INTERFACE IMPORTED)
    set_property(TARGET psimd PROPERTY INTERFACE_LINK_LIBRARIES psimd::psimd)

    find_package(fp16 REQUIRED CONFIG)
    add_library(fp16 INTERFACE IMPORTED)
    set_property(TARGET fp16 PROPERTY INTERFACE_LINK_LIBRARIES fp16::fp16)
endif()

if(USE_TENSORPIPE)
    find_package(tensorpipe REQUIRED CONFIG)
    add_library(tensorpipe INTERFACE IMPORTED)
    set_property(TARGET tensorpipe PROPERTY INTERFACE_LINK_LIBRARIES tensorpipe::tensorpipe)
endif()

if(CONAN_LIBTORCH_USE_SLEEF)
    find_package(sleef REQUIRED CONFIG)
    add_library(sleef INTERFACE IMPORTED)
    set_property(TARGET sleef PROPERTY INTERFACE_LINK_LIBRARIES sleef::sleef)
endif()

if(CONAN_LIBTORCH_USE_PTHREADPOOL)
    find_package(pthreadpool REQUIRED CONFIG)
    add_library(pthreadpool INTERFACE IMPORTED)
    set_property(TARGET pthreadpool PROPERTY INTERFACE_LINK_LIBRARIES pthreadpool::pthreadpool)
endif()

add_subdirectory(source_subfolder)
