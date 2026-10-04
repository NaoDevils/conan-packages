# Conan packages

This repository contains Conan recipes to build some third-party libraries required for the [Nao Devils framework](https://github.com/NaoDevils/CodeRelease).

## libvterm (Conan 2)

`libvterm/0.3.3` packages the MIT-licensed terminal emulation core as a static library for Windows/MSVC and Linux. It exports the CMake target `libvterm::libvterm`. Linux enables position-independent code by default; set `-o "libvterm/*:fPIC=False"` to disable it. No Perl-generated tables or Unix make tools are required: the release archive includes the generated sources, which are built with CMake.

Use Conan 2.3.0 or newer and an existing native compiler profile:

```sh
conan create libvterm --version=0.3.3 --profile:host=default --profile:build=default
```

Run this command natively on each operating system to create the respective binary package. The included `test_package` checks CMake consumption, screen updates, UTF-8 input and terminal erase sequences. Cross-built packages compile the test but only execute it when the host can run the target.

Validated locally with Conan 2.31.2: Windows x86_64/MSVC 194 Release and Linux x86_64/Clang 14 Release, including both package tests.
