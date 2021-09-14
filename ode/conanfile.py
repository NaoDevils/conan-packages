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

    def build(self):
        cmake = CMake(self)
        cmake.definitions["ODE_WITH_DEMOS"] = False
        cmake.definitions["ODE_WITH_TESTS"] = False
        cmake.definitions["ODE_DOUBLE_PRECISION"] = self.options.double_precision
        cmake.configure()
        cmake.build()

    def package(self):
        self.copy("LICENSE*", dst="licenses")
        self.copy("COPYING", dst="licenses")
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "ODE"
        self.cpp_info.names["cmake_find_package_multi"] = "ODE"
        self.cpp_info.names["pkg_config"] = "ode"
        
        if self.options.double_precision:
            name = 'ode_double'
            self.cpp_info.defines = ['dIDEDOUBLE']
        else:
            name = 'ode_single'
            self.cpp_info.defines = ['dIDESINGLE']

        if not self.options.shared:
            name += 's'
        
        if self.settings.build_type == 'Debug':
            name += 'd'
        
        self.cpp_info.libs = [name]
