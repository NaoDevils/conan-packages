from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.files import copy, get
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.43.0"

class LibmpcConan(ConanFile):
    name = "libmpc"
    author = "Aaron Larisch <aaron.larisch@tu-dortmund.de>"
    url = "https://github.com/NaoDevils/conan-packages"
    homepage = "https://github.com/nicolapiccinelli/libmpc"
    description = "Conan package for libmpc++, a C++ library to solve linear and non-linear MPC"
    topics = ("C++", "MPC")
    settings = "os", "compiler", "build_type", "arch"
    no_copy_source = True
        
    def layout(self):
        basic_layout(self)
        
    def package_id(self):
        self.info.clear()
        
    def validate(self):
        if self.settings.compiler.cppstd:
            check_min_cppstd(self, "20")
            
    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination=self.source_folder)

    def requirements(self):
        self.requires("eigen/3.4.0")
        self.requires("nlopt/2.7.1")
        self.requires("osqp/0.6.2")
        
    def generate(self):
        pass

    def build(self):
        pass

    def package(self):
        copy(self, "*", os.path.join(self.source_folder, "include"), os.path.join(self.package_folder, "include"))
