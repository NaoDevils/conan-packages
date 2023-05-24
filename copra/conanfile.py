from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
import os

required_conan_version = ">=1.43.0"

class CopraConan(ConanFile):
    name = "copra"
    author = "Aaron Larisch <aaron.larisch@tu-dortmund.de>"
    url = "https://github.com/NaoDevils/conan-packages"
    homepage = "https://github.com/jrl-umi3218/copra"
    description = "This a c++ implementation of a Time Invariant Linear Model Predictive Controller (LMPC) done in C++14 with python bindings"
    topics = ("C++", "LMPC")
    settings = "os", "compiler", "build_type", "arch"
    license = "BSD-2-Clause"
    
    def layout(self):
        cmake_layout(self)
        
    def source(self):
        git = Git(self)
        clone_args = ['--depth', '1', '--branch', 'v{}'.format(self.version), '--recursive']
        git.clone(url='https://github.com/jrl-umi3218/copra.git', args=clone_args, target='.')
        
    def requirements(self):
        self.requires("eigen/3.4.0")
        self.requires("eigen-quadprog/1.1.1")
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.cache_variables["BUILD_TESTING"] = False
        tc.generate()
        cmake = CMakeDeps(self)
        cmake.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        
    def package_info(self):
        name = "copra"
        if self.settings.build_type == 'Debug':
            name += "_d"
            
        self.cpp_info.libs = [name]
