#!/bin/bash

if [ -z "$1" ]; then
  echo "Usage: $0 <input_file.s>"
  exit 1
fi

base_name="test"

# run generate.py
python3 generate.py

riscv32-unknown-elf-gcc -march=rv32gv -mabi=ilp32 -o "${base_name}.elf" "${base_name}.s"

riscv32-unknown-elf-objdump -d -M numeric,no-aliases "${base_name}.elf" \
| sed -n '/<main>:/,/^$/p' \
| sed '/<main>:/d; /^$/d' \
> "${base_name}.txt"

build/rv32emu -q "${base_name}.elf" \
| grep -E "PC: 0x[0-9a-f]+  Insn: 0x[0-9a-f]+" \
> "${base_name}_emu.txt"

echo "Generated ${base_name}.txt, ${base_name}_emu.txt"

python3 compare.py

echo "Comparison complete. Check output for details."