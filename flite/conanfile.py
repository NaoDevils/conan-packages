from conans import ConanFile, CMake, AutoToolsBuildEnvironment, MSBuild, tools
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
        if self.settings.os == "Windows":
          with tools.chdir(self._source_subfolder + "/sapi"):
            msbuild = MSBuild(self)
            msbuild.build("flite_conan.sln")
        else:        
          with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.make()
                  
    def package(self):
        if self.settings.os == "Windows":
          with tools.chdir(self.package_folder):
            self.copy("*.lib", dst="lib", src=self._source_subfolder, keep_path=False)
            self.copy("*/flite*.h", dst="include/flite", src=self.source_folder, keep_path=False)
            self.copy("*/cst_*.h", dst="include/flite", src=self.source_folder, keep_path=False)
            tools.rename("lib/usenglish.lib", "lib/flite_usenglish.lib")
            tools.rename("lib/cmulex.lib", "lib/flite_cmulex.lib")
        else:
          with tools.chdir(self._source_subfolder):
              autotools = self._configure_autotools()
              autotools.install()
            
          if not self.options.with_utils:
              tools.rmdir(os.path.join(self.package_folder, "bin"))
          
          tools.remove_files_by_mask(os.path.join(self.package_folder, "lib"), "libflite_cmu_*.a")
          
        self.copy("LICENSE*", dst="licenses", src=self._source_subfolder)
        self.copy("COPYING", dst="licenses", src=self._source_subfolder)

    def package_info(self):
        self.cpp_info.libs = ['flite_usenglish','flite_cmulex','flite']
        
        if not self.settings.os == "Windows":
          self.cpp_info.system_libs = ['m']
 