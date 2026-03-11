# duerwen_wakeup_DOA — Conan 1 Paket

Conan-1-Wrapper-Paket für `libduerwen_wakeup_DOA.so`.

| Zielarchitektur | Verwendete Bibliothek |
|---|---|
| `armv7`, `armv7hf`, `armv8` (AArch64) | originale, vorkompilierte `libduerwen_wakeup_DOA.so` |
| alle anderen (x86_64, …) | No-op-Stub, der aus `src/dummy.c` gebaut wird |

## Verzeichnisstruktur

```
conan1/
├── conanfile.py          # Conan-1-Rezept
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

- Conan 1.x (`pip install "conan<2"`)
- CMake ≥ 3.12
- GCC / Clang mit POSIX-Unterstützung (für `pthread.h` in RecvDataCache.h)

## Setup

### 1. ARM-Binary bereitstellen

Die vorkompilierte Bibliothek muss manuell in `lib/` abgelegt werden:

```bash
cp /pfad/zu/libduerwen_wakeup_DOA.so lib/
```

### 2. Paket exportieren

```bash
conan export . duerwen_wakeup_DOA/1.0.0@
```

### 3. Paket installieren (Konsument)

```bash
# ARM (benutzt prebuilt .so)
conan install duerwen_wakeup_DOA/1.0.0@ -s arch=armv8

# x86_64 (baut Stub)
conan install duerwen_wakeup_DOA/1.0.0@ -s arch=x86_64 --build=duerwen_wakeup_DOA
```

### 4. Test-Paket ausführen

```bash
conan test test_package/ duerwen_wakeup_DOA/1.0.0@
```

## Hinweise

- `duerwen_alsa.h` ist **nicht** Teil dieses Pakets – der ALSA-Wrapper ist eine eigene Komponente.
- Der Stub kompiliert ohne jede externe Abhängigkeit außer `pthread` (Standard auf Linux).
- Auf ARM wird **keine** CMake-Build-Phase ausgeführt; die `.so` wird direkt übernommen.
