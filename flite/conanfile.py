from conans import ConanFile, CMake, AutoToolsBuildEnvironment, tools
from conans.errors import ConanInvalidConfiguration
import os

required_conan_version = ">=1.33.0"

class FliteConan(ConanFile):
    name = "flite"
    version = "2.2.1"
    topics = ("flite", "text2speech")
    description = "Flite is a small run-time speech synthesis engine"
    url = "https://github.com/festvox/flite"
    homepage = "http://www.speech.cs.cmu.edu/flite/"
    license = "BSD"

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "fPIC": [True, False],
    }
    default_options = {
        "fPIC": True,
    }

    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"
    _cmake = None
        
    def configure(self):
       del self.settings.compiler.libcxx       
               
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def build(self):    
        autotools = AutoToolsBuildEnvironment(self)
        autotools.fpic = True
        conf_args = []
        conf_args += ["--with-audio=none"]        
        autotools.configure(args=conf_args, configure_dir=self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            autotools.make()
      #      autotools.make(target="get_voices")      
      
    def package(self):
        self.copy("LICENSE*", dst="licenses")
        self.copy("COPYING", dst="licenses")
        
        self.copy(pattern="*.lib", dst="lib", src=self.build_folder , keep_path=False, symlinks=True)
        self.copy(pattern="*.a", dst="lib", src=self.build_folder , keep_path=False, symlinks=True)

        self.copy(pattern="*.flitevox", dst="voices", src=self.build_folder , keep_path=False, symlinks=True)
        
        #self.copy(pattern="*.h", dst="include/flite", src=os.path.join(self.build_folder,"include") , keep_path=True, symlinks=True)
        self.copy(pattern="*.h", dst="include/flite", src=self.source_folder , keep_path=True, symlinks=True)

    def package_info(self):
        self.cpp_info.libs = ['flite']
        
      
