from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import copy, get

import os

required_conan_version = ">=2.3.0"


class LibvtermConan(ConanFile):
    name = "libvterm"
    license = "MIT"
    url = "https://github.com/NaoDevils/conan-packages"
    homepage = "https://www.leonerd.org.uk/code/libvterm/"
    description = "VT220/xterm terminal emulation core"
    package_type = "static-library"
    settings = "os", "arch", "compiler", "build_type"
    exports_sources = "CMakeLists.txt"
    options = {"fPIC": [True, False]}
    default_options = {"fPIC": True}

    def config_options(self):
        if self.settings.os == "Windows":
            self.options.rm_safe("fPIC")

    def configure(self):
        self.settings.compiler.rm_safe("cppstd")
        self.settings.compiler.rm_safe("libcxx")

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        CMakeToolchain(self).generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        CMake(self).install()
        copy(self, "LICENSE", self.source_folder, os.path.join(self.package_folder, "licenses"))

    def package_info(self):
        self.cpp_info.libs = ["vterm"]
        self.cpp_info.set_property("cmake_file_name", "libvterm")
        self.cpp_info.set_property("cmake_target_name", "libvterm::libvterm")
