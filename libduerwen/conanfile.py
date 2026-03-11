import os
from conans import ConanFile, CMake


class DuerwenWakeupDOAConan(ConanFile):
    name = "duerwen_wakeup_DOA"
    version = "1.0.0"
    license = "Proprietary"
    description = (
        "Duerwen Wake-Word Detection and Direction-of-Arrival (DOA) library. "
        "On ARM targets the original prebuilt shared library is used; "
        "on all other architectures a no-op stub is compiled from source."
    )
    url = ""
    settings = "os", "compiler", "arch", "build_type"
    exports_sources = "CMakeLists.txt", "src/*", "include/*", "lib/*"

    @property
    def _is_arm(self):
        """True for any ARM architecture (armv7, armv7hf, armv8 / aarch64, …)."""
        return str(self.settings.arch).startswith("arm")

    def build(self):
        if not self._is_arm:
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def package(self):
        # Always export public headers
        self.copy("*.h", dst="include", src="include")

        if self._is_arm:
            # Use the original prebuilt binary
            self.copy("libduerwen_wakeup_DOA.so", dst="lib", src="lib")
        else:
            # Use the stub built by CMake (searched in build folder)
            self.copy("*.so",   dst="lib", keep_path=False)
            self.copy("*.so.*", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs        = ["duerwen_wakeup_DOA"]
        self.cpp_info.libdirs     = ["lib"]
        self.cpp_info.includedirs = ["include"]
