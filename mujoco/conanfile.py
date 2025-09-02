from conans import ConanFile, tools, CMake

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

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            
    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["MUJOCO_BUILD_TESTS"] = False
        cmake.definitions["MUJOCO_BUILD_TESTS"] = False
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE", dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "MuJoCo"
        self.cpp_info.names["cmake_find_package_multi"] = "MuJoCo"
        self.cpp_info.names["pkg_config"] = "mujoco"
        
        name = self.name
        
        if self.settings.os == "Windows":
            if not self.options.shared:
                name += 's'
            if self.settings.build_type == 'Debug':
                name += 'd'
        
        self.cpp_info.libs = [name]
