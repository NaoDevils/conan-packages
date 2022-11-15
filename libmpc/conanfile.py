from conans import ConanFile, CMake, tools
import os

required_conan_version = ">=1.43.0"

class LibmpcConan(ConanFile):
    name = "libmpc"
    author = "Aaron Larisch <aaron.larisch@tu-dortmund.de>"
    url = "https://github.com/NaoDevils/conan-packages"
    description = "Conan package for libmpc++, a C++ library to solve linear and non-linear MPC"
    topics = ("C++", "MPC")
    settings = "os", "compiler", "build_type", "arch"
    
    exports_sources = "CMakeLists.txt"
    generators = "CMakeDeps"
    
    _cmake = None
    
    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"
    
    def _configure_cmake(self):
        if not self._cmake:
            self._cmake = CMake(self)
            self._cmake.configure(source_folder=self._source_subfolder, build_folder=self._build_subfolder)
        return self._cmake
        
    def validate(self):
        if self.settings.compiler.get_safe("cppstd"):
            tools.check_min_cppstd(self, "20")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self._source_subfolder, strip_root=True)

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()
        
    def requirements(self):
        self.requires("eigen/3.4.0")
        self.requires("nlopt/2.7.1")
        self.requires("osqp/0.6.2")

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        tools.rmdir(os.path.join(self.package_folder, "lib", "cmake"))
