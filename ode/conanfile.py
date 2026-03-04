from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import get, copy
import os

required_conan_version = ">=1.43.0"

class OdeConan(ConanFile):
    name = "ode"

    license = ("LGPL-2.1+", "BSD-3-Clause")
    author = "Aaron Larisch <aaron.larisch@tu-dortmund.de>"
    url = "https://github.com/NaoDevils/conan-packages"
    homepage = "https://www.ode.org"
    description = "ODE is an open source, high performance library for simulating rigid body dynamics."

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "double_precision": [True, False]}
    default_options = {"shared": False, "fPIC": True, "double_precision": True}

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.generator = "Ninja"
        tc.variables["ODE_WITH_DEMOS"] = False
        tc.variables["ODE_WITH_TESTS"] = False
        tc.variables["ODE_DOUBLE_PRECISION"] = self.options.double_precision
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build_requirements(self):
        self.build_requires("ninja/1.10.2")

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "COPYING", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "ODE")
        self.cpp_info.set_property("cmake_target_name", "ode::ode")
        # legacy v1 generator names
        self.cpp_info.names["cmake_find_package"] = "ODE"
        self.cpp_info.names["cmake_find_package_multi"] = "ODE"
        self.cpp_info.names["pkg_config"] = "ode"

        if self.options.double_precision:
            self.cpp_info.defines = ['dIDEDOUBLE']
        else:
            self.cpp_info.defines = ['dIDESINGLE']

        name = self.name

        if self.settings.os == "Windows":
            if self.options.double_precision:
                name += '_double'
            else:
                name += '_single'

            if not self.options.shared:
                name += 's'
            if self.settings.build_type == 'Debug':
                name += 'd'

        self.cpp_info.libs = [name]

        if self.settings.os == 'Linux':
            self.cpp_info.system_libs = ['pthread']
