# duerwen_wakeup_DOA — Conan 2 Paket

Conan-2-Wrapper-Paket für `libduerwen_wakeup_DOA.so`.

| Zielarchitektur | Verwendete Bibliothek |
|---|---|
| `armv7`, `armv7hf`, `armv8` (AArch64) | originale, vorkompilierte `libduerwen_wakeup_DOA.so` |
| alle anderen (x86_64, …) | No-op-Stub, der aus `src/dummy.c` gebaut wird |

## Verzeichnisstruktur

```
conan2/
├── conanfile.py          # Conan-2-Rezept
├── CMakeLists.txt        # Wird nur für den Stub (non-ARM) verwendet
├── src/
│   └── dummy.c           # No-op-Implementierungen aller API-Funktionen
├── include/
│   ├── WakeupApi.h       # Öffentliche Wakeup-/DOA-API
│   └── RecvDataCache.h   # FIFO-Cache-API
├── lib/
│   └── libduerwen_wakeup_DOA.so   # <-- hier die ARM-Binary ablegen (nicht in Git)
└── test_package/         # Smoke-Test für `conan test`
```

## Voraussetzungen

- Conan 2.x (`pip install conan`)
- CMake ≥ 3.15
- GCC / Clang mit POSIX-Unterstützung (für `pthread.h` in RecvDataCache.h)

## Setup

### 1. ARM-Binary bereitstellen

Die vorkompilierte Bibliothek muss manuell in `lib/` abgelegt werden:

```bash
cp /pfad/zu/libduerwen_wakeup_DOA.so lib/
```

### 2. Conan-Profil anlegen (einmalig)

```bash
conan profile detect
```

Für eine ARM-Cross-Build-Umgebung eigenes Profil anlegen, z. B. `~/.conan2/profiles/aarch64-linux`:

```ini
[settings]
os=Linux
arch=armv8
compiler=gcc
compiler.version=11
compiler.libcxx=libstdc++11
build_type=Release

[buildenv]
CC=aarch64-linux-gnu-gcc
CXX=aarch64-linux-gnu-g++
```

### 3. Paket exportieren

```bash
conan export . --version 1.0.0
```

### 4. Paket installieren (Konsument)

```bash
# ARM (benutzt prebuilt .so)
conan install . --profile:host aarch64-linux --profile:build default

# x86_64 (baut Stub)
conan install . --build=duerwen_wakeup_DOA
```

### 5. Test-Paket ausführen

```bash
conan test test_package/ duerwen_wakeup_DOA/1.0.0
```

## CMake-Integration (Konsument)

```cmake
find_package(duerwen_wakeup_DOA REQUIRED)
target_link_libraries(my_target duerwen_wakeup_DOA::duerwen_wakeup_DOA)
```

## Hinweise

- `duerwen_alsa.h` ist **nicht** Teil dieses Pakets – der ALSA-Wrapper ist eine eigene Komponente.
- Der Stub kompiliert ohne jede externe Abhängigkeit außer `pthread` (Standard auf Linux).
- Auf ARM wird **keine** CMake-Build-Phase ausgeführt; die `.so` wird direkt übernommen.
- CMake-Target-Name: `duerwen_wakeup_DOA::duerwen_wakeup_DOA` (gesetzt via `cmake_target_name`).
