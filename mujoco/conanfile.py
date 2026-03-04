from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import get, copy, collect_libs
import os

required_conan_version = ">=2.0.0"

class MuJoCoConan(ConanFile):
    name = "mujoco"

    license = ("Apache-2.0")
    author = "Thomas Klute <thomas.klute@tu-dortmund.de>"
    url = "https://github.com/NaoDevils/conan-packages"
    homepage = "https://mujoco.org/"
    description = "MuJoCo is an open source, high performance library for advanced physics simulation."

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def requirements(self):
        if self.settings.os == "Windows" and self.options.get_safe("shared", True):
            self.requires("msvc-runtime/14.44")

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        cmake_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["MUJOCO_BUILD_TESTS"] = False
        tc.variables["BUILD_SHARED_LIBS"] = self.options.shared
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_file_name", "MuJoCo")
        self.cpp_info.set_property("cmake_target_name", "mujoco::mujoco")
        self.cpp_info.set_property("pkg_config_name", "mujoco")
        self.cpp_info.bindirs = ["bin"]
        self.cpp_info.libs = collect_libs(self)
        self.runenv_info.prepend_path("PATH", os.path.join(self.package_folder, "bin"))
