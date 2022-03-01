from conans import ConanFile, tools, CMake

class OdeConan(ConanFile):
    name = "ode"
    
    license = ("LGPL-2.1+", "BSD-3-Clause")
    author = "Russell L. Smith"
    url = "https://github.com/NaoDevils/conan-packages"
    description = "ODE is an open source, high performance library for simulating rigid body dynamics."
    
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False], "double_precision": [True, False]}
    default_options = {"shared": False, "fPIC": True, "double_precision": True}

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
            
    def _configure_cmake(self):
        cmake = CMake(self, generator="Ninja")
        cmake.definitions["ODE_WITH_DEMOS"] = False
        cmake.definitions["ODE_WITH_TESTS"] = False
        cmake.definitions["ODE_DOUBLE_PRECISION"] = self.options.double_precision
        cmake.configure()
        return cmake

    def build_requirements(self):
        self.build_requires("ninja/1.10.2")

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy("LICENSE*", dst="licenses")
        self.copy("COPYING", dst="licenses")
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
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
