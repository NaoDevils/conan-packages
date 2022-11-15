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
    }
    default_options = {
        "fPIC": True,
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
