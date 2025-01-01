import re
import sys

def parse_pc_range(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    pc_values = []
    for line in lines:
        match = re.match(r"\s*([0-9a-f]+):", line)
        if match:
            pc_values.append(int(match.group(1), 16))
    if not pc_values:
        raise ValueError("No PC values found in the file.")
    
    print(min(pc_values), max(pc_values))
    return min(pc_values), max(pc_values) - 8

def update_emulate_file(emulate_path, pc_start, pc_end):
    with open(emulate_path, 'r') as file:
        content = file.readlines()
    new_content = []
    for line in content:
        if "if (ir->pc < 0x" in line and "|| ir->pc > 0x" in line:
            new_line = f"    if (ir->pc < 0x{pc_start:x} || ir->pc > 0x{pc_end:x})\n"
            new_content.append(new_line)
        else:
            new_content.append(line)
    with open(emulate_path, 'w') as file:
        file.writelines(new_content)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 update_emulate.py <test.txt> <src/emulate.c>")
        sys.exit(1)
    test_txt = sys.argv[1]
    emulate_c = sys.argv[2]
    pc_start, pc_end = parse_pc_range(test_txt)
    update_emulate_file(emulate_c, pc_start, pc_end)
    print(f"Updated {emulate_c} with PC range: 0x{pc_start:x} to 0x{pc_end:x}")
