import os

from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout


class CudnnFrontendTestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "CMakeDeps"

    def requirements(self):
        self.requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure(
            variables={
                "TEST_WITH_CUDNN": self._has_cudnn(),
                "CUDNN_INCLUDE_DIR": self._cudnn_include_dir() or "",
            }
        )
        cmake.build()

    def test(self):
        pass

    def _has_cudnn(self):
        return self._cudnn_include_dir() is not None

    def _cudnn_include_dir(self):
        candidates = []

        env = os.getenv("CUDNN_INCLUDE_DIR")
        if env:
            candidates.append(env)

        cudnn_home = os.getenv("CUDNN_HOME")
        if cudnn_home:
            candidates.append(os.path.join(cudnn_home, "include"))

        for path in candidates:
            if os.path.exists(os.path.join(path, "cudnn.h")):
                return path
        return None