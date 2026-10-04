cmake_minimum_required(VERSION 3.20)
project(libvterm VERSION 0.3.3 LANGUAGES C)

add_library(vterm STATIC
    src/encoding.c src/keyboard.c src/mouse.c src/parser.c src/pen.c
    src/screen.c src/state.c src/unicode.c src/vterm.c)
set_target_properties(vterm PROPERTIES C_STANDARD 11 C_STANDARD_REQUIRED ON)
target_include_directories(vterm PUBLIC include PRIVATE src)
if(MSVC)
    target_compile_definitions(vterm PRIVATE _CRT_SECURE_NO_WARNINGS)
endif()
install(TARGETS vterm ARCHIVE DESTINATION lib)
install(FILES include/vterm.h include/vterm_keycodes.h DESTINATION include)
