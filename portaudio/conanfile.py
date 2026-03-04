from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get, copy, rmdir, collect_libs
from conan.tools.scm import Version
from conan.errors import ConanInvalidConfiguration
import os
import platform

required_conan_version = ">=2.0.0"


class PortaudioConan(ConanFile):
    name = "portaudio"
    topics = ("portaudio", "audio", "recording", "playing")
    description = "PortAudio is a free, cross-platform, open-source, audio I/O library"
    url = "https://github.com/bincrafters/community"
    homepage = "http://www.portaudio.com"
    license = "MIT"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "with_system_alsa": [True, False],
        "with_alsa": [True, False],
        "with_jack": [True, False]
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "with_system_alsa": True,
        "with_alsa": False,
        "with_jack": False
    }

    def validate(self):
        if self.settings.compiler == "apple-clang" and Version(self.settings.compiler.version) < "11":
            raise ConanInvalidConfiguration("This recipe does not support Apple-Clang versions < 11")

    def export_sources(self):
        export_conandata_patches(self)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        if self.settings.os != "Linux":
            del self.options.with_system_alsa
            del self.options.with_alsa
            del self.options.with_jack

    def configure(self):
        try:
            del self.settings.compiler.libcxx
        except Exception:
            pass
        try:
            del self.settings.compiler.cppstd
        except Exception:
            pass

    def requirements(self):
        if self.settings.os == "Linux":
            if self.options.with_alsa:
                self.requires("libalsa/1.1.9")

    def system_requirements(self):
        if self.settings.os == "Linux":
            apt_packages = []
            yum_packages = []
            if self.options.get_safe("with_system_alsa", False):
                apt_packages.append("libasound2-dev")
                yum_packages.append("alsa-lib-devel")
            if self.options.get_safe("with_jack", False):
                apt_packages.append("libjack-dev")
                yum_packages.append("jack-audio-connection-kit-devel")
            if self.settings.arch == "x86" and platform.machine() == "x86_64":
                yum_packages.extend(["glibmm24.i686", "glibc-devel.i686"])
            if apt_packages:
                from conan.tools.system.package_manager import Apt
                Apt(self).install(apt_packages)
            if yum_packages:
                from conan.tools.system.package_manager import Yum
                Yum(self).install(yum_packages)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def layout(self):
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["PA_BUILD_STATIC"] = not self.options.shared
        tc.variables["PA_BUILD_SHARED"] = self.options.shared
        tc.variables["PA_USE_JACK"] = self.options.get_safe("with_jack", False)
        # with_system_alsa=True just makes portaudio use the Linux distro's alsa
        # as a workaround to the fact that conancenter's alsa does not work,
        # at least some of the time (no devices detected by portaudio)
        tc.variables["PA_USE_ALSA"] = self.options.get_safe("with_alsa", False) or self.options.get_safe("with_system_alsa", False)
        tc.generate()
        deps = CMakeDeps(self)
        deps.generate()

    def build(self):
        apply_conandata_patches(self)
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        copy(self, "LICENSE*", src=self.source_folder, dst=os.path.join(self.package_folder, "licenses"))
        cmake = CMake(self)
        cmake.install()
        rmdir(self, os.path.join(self.package_folder, "share"))

    def package_info(self):
        # TODO: Add components with > 19.7, because the next release will most likely have major changes for their CMake setup
        self.cpp_info.libs = collect_libs(self)

        if self.settings.os == "Macos":
            self.cpp_info.frameworks.extend(["CoreAudio", "AudioToolbox", "AudioUnit", "CoreServices", "Carbon"])

        if self.settings.os == "Windows" and self.settings.compiler == "gcc" and not self.options.shared:
            self.cpp_info.system_libs.extend(["winmm", "setupapi"])

        if self.settings.os == "Linux" and not self.options.shared:
            self.cpp_info.system_libs.extend(["m", "pthread"])
            if self.options.get_safe("with_system_alsa", False):
                self.cpp_info.system_libs.append("asound")
            if self.options.get_safe("with_jack", False):
                self.cpp_info.system_libs.append("jack")
