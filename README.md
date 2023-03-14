# RISC-V RV32I[MACF] emulator with ELF support
![GitHub Actions](https://github.com/sysprog21/rv32emu/actions/workflows/main.yml/badge.svg)
```
                       /--===============------\
      ______     __    | |⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺|     |
     |  _ \ \   / /    | |               |     |
     | |_) \ \ / /     | |   Emulator!   |     |
     |  _ < \ V /      | |               |     |
     |_| \_\ \_/       | |_______________|     |
      _________        |                   ::::|
     |___ /___ \       '======================='
       |_ \ __) |      //-'-'-'-'-'-'-'-'-'-'-\\
      ___) / __/      //_'_'_'_'_'_'_'_'_'_'_'_\\
     |____/_____|     [-------------------------]
```

`rv32emu` is an instruction set architecture (ISA) emulator implementing the 32 bit [RISC-V processor model](https://riscv.org/technical/specifications/).

## Build and Verify

`rv32emu` relies on some third-party packages to be fully usable and to provide you full
access to all of its features. Your target system must have a functional [SDL2 library](https://www.libsdl.org/).
* macOS: `brew install sdl2`
* Ubuntu Linux / Debian: `sudo apt install libsdl2-dev`

Install [RISCOF](https://riscof.readthedocs.io/en/stable/installation.html#install-riscof).
```shell
python3 -m pip install git+https://github.com/riscv/riscof
```

Build the emulator.
```shell
make
```

Run sample RV32I[M] programs:
```shell
make check
```

Run [Doom](https://en.wikipedia.org/wiki/Doom_(1993_video_game)), the classical video game, via `rv32emu`:
```shell
make doom
```

The build script will then download data file for Doom automatically.
When Doom is loaded and run, an SDL2-based window ought to appear.

If RV32F support is enabled (turned on by default), [Quake](https://en.wikipedia.org/wiki/Quake_(series)) demo program can be launched via:
```shell
make quake
```

The usage and limitations of Doom and Quake demo are listed in [docs/demo.md](docs/demo.md).

## RISCOF

[RISCOF](https://github.com/riscv-software-src/riscof) - RISC-V Compatibility Framework is a python based framework which enables testing of RISC-V target against a golden reference model. 

The RISC-V Architectural Tests, also known as [riscv-arch-test](https://github.com/riscv-non-isa/riscv-arch-test),
provides the fundamental set of tests that can be used to confirm that the behavior
of the risc-v model adheres to the RISC-V standards while executing certain
applications. (not intended to **replace thorough design verification**)

There are **reference signatures** that generated by the formal RISC-V model [RISC-V SAIL](https://github.com/riscv/sail-riscv)
in the Executable and Linkable Format (ELF) files. ELF files that have multiple
testing instructions, data, and **signatures**, like `cadd-01.elf`. The specific data
places that must be written by the testing model (this emulator) throughout the test are
known as test signatures. The test signatures will be written after it has been completed,
and they will be compared to the reference signature. When both signatures exactly match,
the test is successful.

[RISC-V GNU Compiler Toolchain](https://github.com/riscv-collab/riscv-gnu-toolchain) should be prepared in advance. You can obtain prebuilt GNU toolchain for `riscv32-elf` via [Automated Nightly Release](https://github.com/riscv-collab/riscv-gnu-toolchain/releases). Then, run the following command:
```shell
make arch-test
```

Users of macOS might need to install `sdiff` first.
```shell
brew install diffutils
```

To run the tests for specific extension, set the environmental variable `RISCV_DEVICE` to one of `I`, `M`, `C`, `Zifencei`, `privilege`.
```shell
make arch-test RISCV_DEVICE=I
```

Current progress of this emulator in riscv-arch-test(RV32):
* Passed Tests
    - `I`: Base Integer Instruction Set
    - `M`: Standard Extension for Integer Multiplication and Division
    - `C`: Standard Extension for Compressed Instruction
    - `Zifencei`: Instruction-Fetch Fence
    - `privilege`: RISCV Privileged Specification
* Unsupported tests (runnable but incomplete)
    - `F` Standard Extension for Single-Precision Floating-Point

Detail in riscv-arch-test:
* [RISCOF document](https://riscof.readthedocs.io/en/stable/)
* [riscv-arch-test repository](https://github.com/riscv-non-isa/riscv-arch-test)
* [RISC-V Architectural Testing Framework](https://github.com/riscv-non-isa/riscv-arch-test/blob/master/doc/README.adoc)
* [RISC-V Architecture Test Format Specification](https://github.com/riscv-non-isa/riscv-arch-test/blob/master/spec/TestFormatSpec.adoc)

## Customization

`rv32emu` is configurable, and you can override the below variable(s) to fit your expectations:
* `ENABLE_EXT_M`: Standard Extension for Integer Multiplication and Division
* `ENABLE_EXT_A`: Standard Extension for Atomic Instructions
* `ENABLE_EXT_C`: Standard Extension for Compressed Instructions (RV32C.F excluded)
* `ENABLE_EXT_F`: Standard Extension for Single-Precision Floating Point Instructions
* `ENABLE_Zicsr`: Control and Status Register (CSR)
* `ENABLE_Zifencei`: Instruction-Fetch Fence
* `ENABLE_GDBSTUB` : GDB remote debugging support
* `ENABLE_SDL` : Experimental Display and Event System Calls

e.g., run `make ENABLE_EXT_F=0` for the build without floating-point support.

## GDB Remote Debugging

`rv32emu` is permitted to operate as gdbstub in an experimental manner since it supports
a limited number of [GDB Remote Serial Protocol](https://sourceware.org/gdb/onlinedocs/gdb/Remote-Protocol.html) (GDBRSP).
You must first build the emulator and set `ENABLE_GDBSTUB` to `1` in the `Makefile` in order
to activate this feature. After that, you might execute it using the command below.
```shell
build/rv32emu --gdbstub <binary>
```

The `<binary>` should be the ELF file in RISC-V 32 bit format. Additionally, it is advised
that you compile programs with the `-g` option in order to produce debug information in
your ELF files.

You can run `riscv-gdb` if the emulator starts up correctly without an error. It takes two
GDB commands to connect to the emulator after giving GDB the supported architecture of the
emulator and any debugging symbols it may have.

```shell
$ riscv32-unknown-elf-gdb
(gdb) file <binary>
(gdb) target remote :1234
```

Congratulate yourself if `riscv-gdb` does not produce an error message. Now that the GDB
command line is available, you can communicate with `rv32emu`.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## External sources

In `rv32emu` repository, there are some prebuilt ELF files for testing purpose.
* `aes.elf` : See [tests/aes.c](tests/aes.c)
* `captcha.elf` : See [tests/captcha.c](tests/captcha.c)
* `cc.elf` : See [tests/cc](tests/cc)
* `chacha20.elf` : See [tests/chacha20](tests/chacha20.c)
* `coremark.elf` : See [eembc/coremark](https://github.com/eembc/coremark) [RV32M]
* `dhrystone.elf` : See [rv8-bench](https://github.com/michaeljclark/rv8-bench)
* `doom.elf` : See [sysprog21/doom_riscv](https://github.com/sysprog21/doom_riscv) [RV32M]
* `ieee754.elf` : See [tests/ieee754.c](tests/ieee754.c) [RV32F]
* `jit-bf.elf` : See [ezaki-k/xkon_beta](https://github.com/ezaki-k/xkon_beta)
* `lena.elf`: See [tests/lena.c](tests/lena.c)
* `line.elf` : See [tests/line.c](tests/line.c) [RV32M]
* `maj2random.elf` : See [tests/maj2random.c](tests/maj2random.c) [RV32F]
* `mandelbrot.elf` : See [tests/mandelbrot.c](tests/mandelbrot.c)
* `nqueens.elf` : See [tests/nqueens.c](tests/nqueens.c)
* `nyancat.elf` : See [tests/nyancat.c](tests/nyancat.c)
* `pi.elf` : See [tests/pi.c](tests/pi.c) [RV32M]
* `qrcode.elf` : See [tests/qrcode.c](tests/qrcode.c)
* `quake.elf` : See [sysprog21/quake-embedded](https://github.com/sysprog21/quake-embedded) [RV32F]
* `richards.elf` : See [tests/richards.c](tests/richards.c)
* `scimark2.elf` : See [tests/scimark2](tests/scimark2) [RV32MF]

## Reference

* [Writing a simple RISC-V emulator in plain C](https://fmash16.github.io/content/posts/riscv-emulator-in-c.html)
* [Writing a RISC-V Emulator in Rust](https://book.rvemu.app/)
* [Juraj's RISC-V note](https://jborza.com/tags/riscv/)
* [libriscv: RISC-V userspace emulator library](https://github.com/fwsGonzo/libriscv)
* [LupV: an education-friendly RISC-V based system emulator](https://gitlab.com/luplab/lupv)
* [mini-rv32ima](https://github.com/cnlohr/mini-rv32ima)
* [yutongshen/RISC-V-Simulator](https://github.com/yutongshen/RISC-V-Simulator)
* [rvc](https://github.com/PiMaker/rvc)
* [RVVM](https://github.com/LekKit/RVVM)
* [Threaded Code](https://www.complang.tuwien.ac.at/forth/threaded-code.html) / [threaded-code-benchmark](https://github.com/shadowofneptune/threaded-code-benchmark)

## License
`rv32emu` is available under a permissive MIT-style license.
Use of this source code is governed by a MIT license that can be found in the [LICENSE](LICENSE) file.
