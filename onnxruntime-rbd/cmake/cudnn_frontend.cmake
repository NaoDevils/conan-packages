# Try Conan/CMake-provided cudnn_frontend first.
find_package(cudnn_frontend CONFIG QUIET)
if(TARGET cudnn_frontend::cudnn_frontend)
  get_target_property(_fe_link cudnn_frontend::cudnn_frontend INTERFACE_LINK_LIBRARIES)
  get_target_property(_fe_inc cudnn_frontend::cudnn_frontend INTERFACE_INCLUDE_DIRECTORIES)
  message(STATUS "DEBUG cudnn_frontend::cudnn_frontend LINK='${_fe_link}'")
  message(STATUS "DEBUG cudnn_frontend::cudnn_frontend INCLUDE='${_fe_inc}'")
else()
  message(STATUS "DEBUG cudnn_frontend::cudnn_frontend NOT FOUND")
endif()

if(TARGET cudnn-frontend_DEPS_TARGET)
  get_target_property(_fe_deps_link cudnn-frontend_DEPS_TARGET INTERFACE_LINK_LIBRARIES)
  get_target_property(_fe_deps_inc cudnn-frontend_DEPS_TARGET INTERFACE_INCLUDE_DIRECTORIES)
  get_target_property(_fe_deps_type cudnn-frontend_DEPS_TARGET TYPE)
  message(STATUS "DEBUG cudnn-frontend_DEPS_TARGET TYPE='${_fe_deps_type}'")
  message(STATUS "DEBUG cudnn-frontend_DEPS_TARGET LINK='${_fe_deps_link}'")
  message(STATUS "DEBUG cudnn-frontend_DEPS_TARGET INCLUDE='${_fe_deps_inc}'")
else()
  message(STATUS "DEBUG cudnn-frontend_DEPS_TARGET NOT FOUND")
endif()

if(cudnn_frontend_FOUND)
  message(STATUS "Using cudnn_frontend from find_package()")

  if(NOT TARGET cudnn_frontend::cudnn_frontend)
    message(FATAL_ERROR "cudnn_frontend package found, but target cudnn_frontend::cudnn_frontend is missing.")
  endif()
else()
  message(STATUS "cudnn_frontend not found via find_package(), falling back to FetchContent")

  onnxruntime_fetchcontent_declare(
    cudnn_frontend
    URL ${DEP_URL_cudnn_frontend}
    URL_HASH SHA1=${DEP_SHA1_cudnn_frontend}
    EXCLUDE_FROM_ALL
  )

  set(CUDNN_FRONTEND_BUILD_SAMPLES OFF CACHE BOOL "" FORCE)
  set(CUDNN_FRONTEND_BUILD_TESTS OFF CACHE BOOL "" FORCE)
  set(CUDNN_FRONTEND_BUILD_PYTHON_BINDINGS OFF CACHE BOOL "" FORCE)
  set(CUDNN_FRONTEND_SKIP_JSON_LIB OFF CACHE BOOL "" FORCE)

  if(onnxruntime_CUDNN_HOME)
    set(CUDNN_PATH ${onnxruntime_CUDNN_HOME})
  endif()

  onnxruntime_fetchcontent_makeavailable(cudnn_frontend)

  if(NOT TARGET cudnn_frontend::cudnn_frontend)
    message(FATAL_ERROR "Fetched cudnn_frontend, but target cudnn_frontend::cudnn_frontend was not created.")
  endif()
endif()

# ---- cuDNN discovery for ORT ----
set(_ORT_CUDNN_ROOT "${onnxruntime_CUDNN_HOME}")
if(NOT _ORT_CUDNN_ROOT)
  set(_ORT_CUDNN_ROOT "$ENV{CUDNN_HOME}")
endif()

if(NOT _ORT_CUDNN_ROOT)
  message(FATAL_ERROR "Neither onnxruntime_CUDNN_HOME nor CUDNN_HOME is set")
endif()

# Clear stale cache from previous runs
unset(CUDNN_INCLUDE_DIR CACHE)
unset(CUDNN_INCLUDE_DIR)

message(STATUS "onnxruntime_CUDNN_HOME='${onnxruntime_CUDNN_HOME}'")
message(STATUS "_ORT_CUDNN_ROOT='${_ORT_CUDNN_ROOT}'")

# Prefer the exact known sysroot layout first
if(EXISTS "/sysroot/usr/include/cudnn.h")
  set(CUDNN_INCLUDE_DIR "/sysroot/usr/include")
elseif(EXISTS "${_ORT_CUDNN_ROOT}/include/cudnn.h")
  set(CUDNN_INCLUDE_DIR "${_ORT_CUDNN_ROOT}/include")
elseif(EXISTS "${_ORT_CUDNN_ROOT}/include/aarch64-linux-gnu/cudnn.h")
  set(CUDNN_INCLUDE_DIR "${_ORT_CUDNN_ROOT}/include/aarch64-linux-gnu")
endif()

message(STATUS "CUDNN_INCLUDE_DIR='${CUDNN_INCLUDE_DIR}'")

if(EXISTS "/sysroot/usr/include/cudnn.h")
  message(STATUS "/sysroot/usr/include/cudnn.h exists")
else()
  message(STATUS "/sysroot/usr/include/cudnn.h does NOT exist")
endif()

if(NOT CUDNN_INCLUDE_DIR)
  message(FATAL_ERROR "Could not find cudnn.h. onnxruntime_CUDNN_HOME='${onnxruntime_CUDNN_HOME}'")
endif()

set(_CUDNN_VERSION_HEADER "${CUDNN_INCLUDE_DIR}/cudnn_version.h")
if(EXISTS "${_CUDNN_VERSION_HEADER}")
  file(READ "${_CUDNN_VERSION_HEADER}" _CUDNN_VER_CONTENT)

  string(REGEX MATCH "#define CUDNN_MAJOR[ \t]+([0-9]+)" _match_major "${_CUDNN_VER_CONTENT}")
  set(CUDNN_MAJOR_VERSION "${CMAKE_MATCH_1}")

  string(REGEX MATCH "#define CUDNN_MINOR[ \t]+([0-9]+)" _match_minor "${_CUDNN_VER_CONTENT}")
  set(CUDNN_MINOR_VERSION "${CMAKE_MATCH_1}")

  string(REGEX MATCH "#define CUDNN_PATCHLEVEL[ \t]+([0-9]+)" _match_patch "${_CUDNN_VER_CONTENT}")
  set(CUDNN_PATCH_VERSION "${CMAKE_MATCH_1}")
endif()

message(STATUS "cuDNN version: ${CUDNN_MAJOR_VERSION}.${CUDNN_MINOR_VERSION}.${CUDNN_PATCH_VERSION}")

unset(CUDNN_LIBRARY_MAIN CACHE)
unset(CUDNN_LIBRARY_MAIN)

if(EXISTS "/sysroot/usr/lib/aarch64-linux-gnu/libcudnn.so")
  set(CUDNN_LIBRARY_MAIN "/sysroot/usr/lib/aarch64-linux-gnu/libcudnn.so")
elseif(EXISTS "${_ORT_CUDNN_ROOT}/lib/aarch64-linux-gnu/libcudnn.so")
  set(CUDNN_LIBRARY_MAIN "${_ORT_CUDNN_ROOT}/lib/aarch64-linux-gnu/libcudnn.so")
elseif(EXISTS "${_ORT_CUDNN_ROOT}/lib/libcudnn.so")
  set(CUDNN_LIBRARY_MAIN "${_ORT_CUDNN_ROOT}/lib/libcudnn.so")
elseif(EXISTS "${_ORT_CUDNN_ROOT}/lib64/libcudnn.so")
  set(CUDNN_LIBRARY_MAIN "${_ORT_CUDNN_ROOT}/lib64/libcudnn.so")
endif()

message(STATUS "CUDNN_LIBRARY_MAIN='${CUDNN_LIBRARY_MAIN}'")

if(NOT CUDNN_LIBRARY_MAIN)
  message(FATAL_ERROR "Could not find libcudnn. onnxruntime_CUDNN_HOME='${onnxruntime_CUDNN_HOME}'")
endif()

function(_ort_pick_cudnn_lib outvar name)
  if(EXISTS "/sysroot/usr/lib/aarch64-linux-gnu/lib${name}.so")
    set(${outvar} "/sysroot/usr/lib/aarch64-linux-gnu/lib${name}.so" PARENT_SCOPE)
  elseif(EXISTS "${_ORT_CUDNN_ROOT}/lib/aarch64-linux-gnu/lib${name}.so")
    set(${outvar} "${_ORT_CUDNN_ROOT}/lib/aarch64-linux-gnu/lib${name}.so" PARENT_SCOPE)
  elseif(EXISTS "${_ORT_CUDNN_ROOT}/lib/lib${name}.so")
    set(${outvar} "${_ORT_CUDNN_ROOT}/lib/lib${name}.so" PARENT_SCOPE)
  elseif(EXISTS "${_ORT_CUDNN_ROOT}/lib64/lib${name}.so")
    set(${outvar} "${_ORT_CUDNN_ROOT}/lib64/lib${name}.so" PARENT_SCOPE)
  endif()
endfunction()

_ort_pick_cudnn_lib(CUDNN_LIBRARY_CNN cudnn_cnn)
_ort_pick_cudnn_lib(CUDNN_LIBRARY_OPS cudnn_ops)
_ort_pick_cudnn_lib(CUDNN_LIBRARY_ADV cudnn_adv)
_ort_pick_cudnn_lib(CUDNN_LIBRARY_GRAPH cudnn_graph)
_ort_pick_cudnn_lib(CUDNN_LIBRARY_HEURISTIC cudnn_heuristic)
_ort_pick_cudnn_lib(CUDNN_LIBRARY_ENGINES_PRECOMP cudnn_engines_precompiled)
_ort_pick_cudnn_lib(CUDNN_LIBRARY_ENGINES_RUNTIME cudnn_engines_runtime_compiled)

if(NOT TARGET CUDNN::cudnn_all)
  add_library(CUDNN::cudnn_all INTERFACE IMPORTED)
  target_include_directories(CUDNN::cudnn_all INTERFACE "${CUDNN_INCLUDE_DIR}")

  if(TARGET cudnn_frontend::cudnn_frontend)
    get_target_property(_cudnnfe_includes cudnn_frontend::cudnn_frontend INTERFACE_INCLUDE_DIRECTORIES)
    if(_cudnnfe_includes)
      target_include_directories(CUDNN::cudnn_all INTERFACE ${_cudnnfe_includes})
    endif()
  endif()

  target_link_libraries(CUDNN::cudnn_all INTERFACE
    "${CUDNN_LIBRARY_MAIN}"
    $<$<BOOL:${CUDNN_LIBRARY_CNN}>:${CUDNN_LIBRARY_CNN}>
    $<$<BOOL:${CUDNN_LIBRARY_OPS}>:${CUDNN_LIBRARY_OPS}>
    $<$<BOOL:${CUDNN_LIBRARY_ADV}>:${CUDNN_LIBRARY_ADV}>
    $<$<BOOL:${CUDNN_LIBRARY_GRAPH}>:${CUDNN_LIBRARY_GRAPH}>
    $<$<BOOL:${CUDNN_LIBRARY_HEURISTIC}>:${CUDNN_LIBRARY_HEURISTIC}>
    $<$<BOOL:${CUDNN_LIBRARY_ENGINES_PRECOMP}>:${CUDNN_LIBRARY_ENGINES_PRECOMP}>
    $<$<BOOL:${CUDNN_LIBRARY_ENGINES_RUNTIME}>:${CUDNN_LIBRARY_ENGINES_RUNTIME}>
  )

  get_target_property(_cudnn_all_link CUDNN::cudnn_all INTERFACE_LINK_LIBRARIES)
  get_target_property(_cudnn_all_inc CUDNN::cudnn_all INTERFACE_INCLUDE_DIRECTORIES)
  message(STATUS "DEBUG CUDNN::cudnn_all LINK='${_cudnn_all_link}'")
  message(STATUS "DEBUG CUDNN::cudnn_all INCLUDE='${_cudnn_all_inc}'")
endif()