from conan import ConanFile
from conan.tools.files import copy, get
import os

required_conan_version = ">=2"


class CudnnFrontendConan(ConanFile):
    name = "cudnn-frontend"
    version = "1.15.0"
    package_type = "header-library"
    
    license = "MIT"
    url = "https://github.com/NVIDIA/cudnn-frontend"
    homepage = "https://github.com/NVIDIA/cudnn-frontend"
    description = "NVIDIA cuDNN C++ Frontend API"
    topics = ("cudnn", "cuda", "nvidia", "header-only")

    package_type = "header-library"
    settings = "os", "arch", "compiler", "build_type"
    no_copy_source = True

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def package_id(self):
        self.info.clear()

    def package(self):
        copy(
            self,
            pattern="*",
            src=os.path.join(self.source_folder, "include"),
            dst=os.path.join(self.package_folder, "include"),
        )
        copy(
            self,
            pattern="LICENSE*",
            src=self.source_folder,
            dst=os.path.join(self.package_folder, "licenses"),
            keep_path=False,
        )

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = []
        self.cpp_info.bindirs = []

        self.cpp_info.set_property("cmake_file_name", "cudnn_frontend")
        self.cpp_info.set_property("cmake_target_name", "cudnn_frontend::cudnn_frontend")
        self.cpp_info.set_property("pkg_config_name", "cudnn_frontend")