from conans import ConanFile, CMake, tools
import os

class OsqpConan(ConanFile):
    name = "osqp"
    license = "MIT"
    author = "Aaron Larisch <aaron.larisch@tu-dortmund.de>"
    url = "https://github.com/NaoDevils/conan-packages"
    description = "Conan package for the OSQP library, the Operator Splitting QP solver"
    topics = ("C++", "QP", "Solver")
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    
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

    _cmake = None
    
    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"
        
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            
    def source(self):
        git = tools.Git(folder=self._source_subfolder)
        git.clone("https://github.com/osqp/osqp.git")
        git.checkout("v{}".format(self.version), submodule="recursive")
            
    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            if self.options.embedded:
                self._cmake.definitions["EMBEDDED"] = self.options.embedded
            self._cmake.definitions["PRINTING"] = self.options.printing
            self._cmake.definitions["PROFILING"] = self.options.profiling
            self._cmake.definitions["CTRLC"] = self.options.ctrlc
            self._cmake.definitions["DFLOAT"] = self.options.dfloat
            self._cmake.definitions["DLONG"] = self.options.dlong
            self._cmake.definitions["DEBUG"] = self.options.debug
            self._cmake.definitions["COVERAGE"] = self.options.coverage
            self._cmake.definitions["ENABLE_MKL_PARDISO"] = self.options.mkl_paradiso
            self._cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
            
    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))

    def package_info(self):
        self.cpp_info.libs = ["osqp", "qdldl"]
