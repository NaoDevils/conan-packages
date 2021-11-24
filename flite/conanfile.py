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
        "shared": [True, False],
        "fPIC": [True, False],
        "with_utils": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_utils": False,
    }

    _source_subfolder = "source_subfolder"
    _autotools = None
        
    def configure(self):
       del self.settings.compiler.libcxx       
               
    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)
        
    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
            
        self._autotools = AutoToolsBuildEnvironment(self)
        self._autotools.configure(args=["--with-audio=none"])
        return self._autotools

    def build(self):    
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.make()
      
    def package(self):
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.install()
            
        if not self.options.with_utils:
            tools.rmdir(os.path.join(self.package_folder, "bin"))
            
        # TODO: Remove libflite_cmu_*.a ?
        
        self.copy("LICENSE*", dst="licenses", src=self._source_subfolder)
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ['flite_usenglish','flite_cmulex','flite']
        
        self.cpp_info.system_libs = ['m']
 