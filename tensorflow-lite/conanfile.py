from conans import ConanFile, tools, CMake

class OdeConan(ConanFile):
    name = "tensorflow-lite"
    repo_url = "https://github.com/tensorflow/tensorflow.git"
    
    license = ("Apache-2.0")
    author = "Google Inc."
    url = "https://github.com/NaoDevils/conan-packages"
    description = "TensorFlow is an end-to-end open source platform for machine learning."
    
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    def source(self):
       tools.get(**self.conan_data["sources"][self.version], destination=self.source_folder, strip_root=True)
    
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build(self):
        cmake = CMake(self)
        cmake.generator = "Ninja"
        cmake.configure(source_folder="tensorflow/lite")
        cmake.build()

    def package(self):
        self.copy("LICENSE*", dst="licenses")
        self.copy("COPYING", dst="licenses")
        
        # we do not seem to need the abseil library
        self.copy(pattern="*.dll", dst="bin", src=self.build_folder , keep_path=False, symlinks=True, excludes="absl_*")
        self.copy(pattern="*.lib", dst="lib", src=self.build_folder , keep_path=False, symlinks=True, excludes="absl_*")
        self.copy(pattern="*.so", dst="lib", src=self.build_folder , keep_path=False, symlinks=True, excludes="absl_*")
        self.copy(pattern="*.a", dst="lib", src=self.build_folder , keep_path=False, symlinks=True, excludes="absl_*")
        
        self.copy("*.h", dst="include/tensorflow/lite", src="{}/tensorflow/lite/".format(self.source_folder), keep_path=True, symlinks=True)
        self.copy("*.h", dst="include/flatbuffers", src="{}/flatbuffers/include/flatbuffers".format(self.build_folder), keep_path=True, symlinks=True)

    def package_info(self):
        self.cpp_info.libs = ['clog', 'cpuinfo', 'farmhash', 'fft2d_fftsg', 'fft2d_fftsg2d', 'flatbuffers', 'pthreadpool', 'ruy', 'tensorflow-lite', 'XNNPACK']
