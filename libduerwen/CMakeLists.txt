cmake_minimum_required(VERSION 3.12)
project(duerwen_wakeup_DOA VERSION 1.0.0 LANGUAGES C)

# ---------------------------------------------------------------------------
# This CMakeLists.txt is only invoked for non-ARM platforms to build the
# no-op stub library.  On ARM the Conan recipe uses the prebuilt .so directly.
# ---------------------------------------------------------------------------

add_library(${PROJECT_NAME} SHARED
    src/dummy.c
)

target_include_directories(${PROJECT_NAME}
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include>
)

set_target_properties(${PROJECT_NAME} PROPERTIES
    VERSION   ${PROJECT_VERSION}
    SOVERSION 1
)
