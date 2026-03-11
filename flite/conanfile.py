from conan import ConanFile
from conan.tools.gnu import Autotools, AutotoolsToolchain
from conan.tools.microsoft import MSBuild
from conan.tools.files import (
    get, copy, chdir, rename, rmdir, rm, replace_in_file
)
from conan.tools.layout import basic_layout
import os

required_conan_version = ">=1.43.0"

class FliteConan(ConanFile):
    name = "flite"
    version = "2.2.1"
    topics = ("flite", "text2speech")
    description = "Flite is a small run-time speech synthesis engine"
    url = "https://github.com/NaoDevils/conan-packages"
    homepage = "https://github.com/festvox/flite"
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

    def build_requirements(self):
        if self.settings.os != "Windows":
            self.build_requires("make/4.3")  # Make 4.4 is currently incompatible

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        try:
            del self.settings.compiler.libcxx
        except Exception:
            pass

    def layout(self):
        basic_layout(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True, destination=self._source_subfolder)

    def generate(self):
        if self.settings.os != "Windows":
            tc = AutotoolsToolchain(self)
            tc.configure_args.append("--with-audio=none")
            tc.generate()
    def _patch_sln_build_type(self):
        """Patch flite_conan.sln to accept build types beyond Debug and Release.

        The upstream solution only defines Debug|x64 and Release|x64 configurations.
        When Conan requests RelWithDebInfo or MinSizeRel, MSBuild fails with
        MSB4126 (invalid solution configuration). We add the missing solution-level
        entry and map each project's configuration to the nearest base config.
        """
        build_type = str(self.settings.build_type)
        if build_type in ("Debug", "Release"):
            return

        base_config = "Release" if build_type in ("RelWithDebInfo", "MinSizeRel") else "Debug"

        from conan.tools.files import load, save
        import re

        sln_path = os.path.join(self.source_folder, self._source_subfolder, "sapi", "flite_conan.sln")
        if not os.path.exists(sln_path):
            return

        content = load(self, sln_path)

        # 1. Add solution-level configuration entry (only if not already present)
        new_entry = f"\t\t{build_type}|x64 = {build_type}|x64\n"
        if new_entry not in content:
            old = f"\t\t{base_config}|x64 = {base_config}|x64\n"
            content = content.replace(old, old + new_entry)

        # 2. Add project-level mapping entries for each GUID so MSBuild knows
        #    which project configuration to build for the new solution config.
        pattern = re.compile(
            r'(\t\t\{[0-9A-Fa-f\-]+\})\.' + re.escape(base_config) + r'\|x64\.Build\.0 = ' + re.escape(base_config) + r'\|x64'
        )

        def add_mapping(m):
            prefix = m.group(1)
            new_active = f"\n{prefix}.{build_type}|x64.ActiveCfg = {base_config}|x64"
            new_build  = f"\n{prefix}.{build_type}|x64.Build.0 = {base_config}|x64"
            # Only add if not already present
            if f"{prefix}.{build_type}|x64.ActiveCfg" in content:
                return m.group(0)
            return m.group(0) + new_active + new_build

        content = pattern.sub(add_mapping, content)

        save(self, sln_path, content)

    def _patch_windows_toolset(self):
        """Patch vcxproj toolset to match the detected MSVC version.

        Upstream .vcxproj files target v142 (VS2019). When building with VS2022
        (msvc >= 193), MSBuild fails unless VS2019 build tools are installed.
        We patch the project files to v143 so they build with VS2022 toolchain.

        Note: conan.tools.files.replace_in_file() is strict and raises if the
        pattern isn't present. Some projects use only one of the representations,
        so we patch by loading and saving the file when a change is actually made.
        """
        if self.settings.compiler != "msvc":
            return

        # MSVC 19.3x/19.4x -> VS2022 toolset v143
        try:
            msvc_ver = int(str(self.settings.compiler.version))
        except Exception:
            msvc_ver = None

        desired_toolset = "v143" if (msvc_ver is None or msvc_ver >= 193) else None
        if not desired_toolset:
            return

        from conan.tools.files import load, save

        sapi_dir = os.path.join(self.source_folder, self._source_subfolder, "sapi")
        for root, _, files in os.walk(sapi_dir):
            for fn in files:
                if not fn.lower().endswith(".vcxproj"):
                    continue
                vcxproj = os.path.join(root, fn)
                content = load(self, vcxproj)

                new_content = content
                new_content = new_content.replace(
                    "<PlatformToolset>v142</PlatformToolset>",
                    f"<PlatformToolset>{desired_toolset}</PlatformToolset>"
                )
                new_content = new_content.replace(
                    'PlatformToolset="v142"',
                    f'PlatformToolset="{desired_toolset}"'
                )

                if new_content != content:
                    save(self, vcxproj, new_content)

    def build(self):
        if self.settings.os == "Windows":
            self._patch_sln_build_type()
            self._patch_windows_toolset()
            with chdir(self, os.path.join(self.source_folder, self._source_subfolder, "sapi")):
                msbuild = MSBuild(self)
                msbuild.build("flite_conan.sln")
        else:
            src = os.path.join(self.source_folder, self._source_subfolder)
            with chdir(self, src):
                autotools = Autotools(self)
                # Run configure from the source folder so generated files land next to Makefile
                autotools.configure(build_script_folder=src)
                autotools.make()

    def package(self):
        if self.settings.os == "Windows":
            copy(self, "*.lib",
                 src=os.path.join(self.source_folder, self._source_subfolder),
                 dst=os.path.join(self.package_folder, "lib"),
                 keep_path=False)
            copy(self, "*/flite*.h",
                 src=self.source_folder,
                 dst=os.path.join(self.package_folder, "include", "flite"),
                 keep_path=False)
            copy(self, "*/cst_*.h",
                 src=self.source_folder,
                 dst=os.path.join(self.package_folder, "include", "flite"),
                 keep_path=False)
            rename(self,
                   os.path.join(self.package_folder, "lib", "usenglish.lib"),
                   os.path.join(self.package_folder, "lib", "flite_usenglish.lib"))
            rename(self,
                   os.path.join(self.package_folder, "lib", "cmulex.lib"),
                   os.path.join(self.package_folder, "lib", "flite_cmulex.lib"))
        else:
            src = os.path.join(self.source_folder, self._source_subfolder)
            with chdir(self, src):
                autotools = Autotools(self)
                autotools.install()

            if not self.options.with_utils:
                rmdir(self, os.path.join(self.package_folder, "bin"))

            rm(self, "libflite_cmu_*.a", os.path.join(self.package_folder, "lib"))

        copy(self, "LICENSE*",
             src=os.path.join(self.source_folder, self._source_subfolder),
             dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "COPYING",
             src=os.path.join(self.source_folder, self._source_subfolder),
             dst=os.path.join(self.package_folder, "licenses"))

    def package_info(self):
        self.cpp_info.libs = ['flite_usenglish', 'flite_cmulex', 'flite']

        if self.settings.os in ("Linux", "FreeBSD"):
            # flite uses math functions (exp/log/sqrt/pow) -> libm
            self.cpp_info.system_libs.append("m")
