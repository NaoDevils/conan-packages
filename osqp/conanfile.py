from conan import ConanFile
from conan.tools.scm import Git
from conan.tools.cmake import CMake, CMakeToolchain, cmake_layout
from conan.tools.files import rmdir
import os

class OsqpConan(ConanFile):
    name = "osqp"
    license = ("Apache-2.0")
    author = "Aaron Larisch <aaron.larisch@tu-dortmund.de>"
    url = "https://github.com/NaoDevils/conan-packages"
    homepage = "https://osqp.org"
    description = "Conan package for the OSQP library, the Operator Splitting QP solver"
    topics = ("C++", "QP", "Solver")
    settings = "os", "compiler", "build_type", "arch"
    
    options = {
        "fPIC": [True, False],
        "embedded": [False, 1, 2],
        "printing": [True, False],
        "profiling": [True, False],
        "ctrlc": [True, False],
        "dfloat": [True, False],
        "dlong": [True, False],
        "debug": [True, False],
        "coverage": [True, False],
        "mkl_paradiso": [True, False],
    }
    default_options = {
        "fPIC": True,
        "embedded": False,
        "printing": True,
        "profiling": True,
        "ctrlc": True,
        "dfloat": False,
        "dlong": True,
        "debug": False,
        "coverage": False,
        "mkl_paradiso": True,
    }
        
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            
    def source(self):
        git = Git(self)
        clone_args = ['--depth', '1', '--branch', 'v{}'.format(self.version), '--recursive']
        git.clone(url='https://github.com/osqp/osqp.git', args=clone_args, target='.')
        
    def layout(self):
        cmake_layout(self)
        
    def generate(self):
        tc = CMakeToolchain(self)
        if self.options.embedded:
            tc.variables["EMBEDDED"] = self.options.embedded
        tc.variables["PRINTING"] = self.options.printing
        tc.variables["PROFILING"] = self.options.profiling
        tc.variables["CTRLC"] = self.options.ctrlc
        tc.variables["DFLOAT"] = self.options.dfloat
        tc.variables["DLONG"] = self.options.dlong
        tc.variables["DEBUG"] = self.options.debug
        tc.variables["COVERAGE"] = self.options.coverage
        tc.variables["ENABLE_MKL_PARDISO"] = self.options.mkl_paradiso
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        
    def package(self):
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.libs = ["osqp", "qdldl"]
