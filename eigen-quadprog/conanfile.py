from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.files import apply_conandata_patches, export_conandata_patches, copy
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
import os

required_conan_version = ">=1.43.0"

class EigenQuadprogConan(ConanFile):
    name = "eigen-quadprog"
    author = "Aaron Larisch <aaron.larisch@tu-dortmund.de>"
    url = "https://github.com/NaoDevils/conan-packages"
    homepage = "https://github.com/jrl-umi3218/eigen-quadprog"
    description = "eigen-quadprog allow to use the QuadProg QP solver with the Eigen3 library."
    topics = ("C++", "QuadProg")
    settings = "os", "compiler", "build_type", "arch"
    license = ("LGPL-3")
    
    _source_subfolder = "source_subfolder"
    
    def export_sources(self):
        export_conandata_patches(self)
        
    def layout(self):
        cmake_layout(self)
        
    def source(self):
        git = Git(self)
        clone_args = ['--depth', '1', '--branch', 'v{}'.format(self.version), '--recursive']
        git.clone(url='https://github.com/jrl-umi3218/eigen-quadprog.git', args=clone_args, target=self._source_subfolder)
        
    def requirements(self):
        self.requires("eigen/3.4.0")
        self.requires("libf2c/20181026")
        
    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["USE_F2C"] = True
        tc.variables["USE_FORTRAN_SUBDIRECTORY"] = False
        tc.variables["BUILD_TESTING"] = False
        tc.generate()
        cmake = CMakeDeps(self)
        cmake.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure(build_script_folder=self._source_subfolder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()
        
    def package_info(self):
        name = "eigen-quadprog"
        if self.settings.build_type == 'Debug':
            name += "_d"
            
        self.cpp_info.libs = [name]
