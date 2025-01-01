import re
import argparse

def parse_emulator_line(line):
    match = re.match(r"PC: 0x([0-9a-f]+)\s+Insn: 0x([0-9a-f]+)\s+(\S+)\s+RS1: (\d+)\s+RS2: (\d+)\s+RD: (\d+)\s+VS1: (\d+)\s+VS2: (\d+)\s+VS3: (\d+)\s+VD: (\d+)\s+VM: (\d+)\s+Imm: (-?\d+)", line)
    if not match:
        return None

    pc = hex(int(match.group(1), 16))  # Convert PC to hex without leading zeros
    opcode = match.group(3)

    if not opcode.startswith('v'):
        return None

    entry = {
        "opcode": re.sub(r'_', '.', opcode),
        "rs1": int(match.group(4)),
        "rs2": int(match.group(5)),
        "rd": int(match.group(6)),
        "vs1": int(match.group(7)),
        "vs2": int(match.group(8)),
        "vs3": int(match.group(9)),
        "vd": int(match.group(10)),
        "vm": int(match.group(11)),
        "imm": int(match.group(12)),
    }

    return pc, entry

def parse_emulator_file(filepath):
    emulator_dict = {}
    with open(filepath, "r") as file:
        lines = file.readlines()
        for line in lines:
            parsed = parse_emulator_line(line)
            if parsed:
                pc, entry = parsed
                emulator_dict[pc] = entry
    return emulator_dict

def parse_objdump_line(line):
    match = re.match(r"\s*([0-9a-f]+):\s+([0-9a-f]+)\s+(\S+)\s+v(\d+),\(x(\d+)\)(?:,v(\d+)|,x(\d+))?", line)
    if not match:
        return None

    pc = hex(int(match.group(1), 16))  # Convert PC to hex without leading zeros
    opcode = match.group(3)
    vd = int(match.group(4)) if opcode.startswith('vl') else 0
    vs3 = int(match.group(4)) if opcode.startswith('vs') else 0
    rs1 = int(match.group(5))
    vs2 = int(match.group(6)) if match.group(6) else 0
    rs2 = int(match.group(7)) if match.group(7) else 0

    entry = {
        "opcode": opcode,
        "vd": vd,
        "rs1": rs1,
        "vs2": vs2,
        "rs2": rs2,
        "rd": 0,
        "vs1": 0,
        "vs3": vs3,
        "vm": 1,
        "imm": 0,
    }

    return pc, entry

def parse_objdump_opi_line(line):
    match = re.match(r"\s*([0-9a-f]+):\s+([0-9a-f]+)\s+(\S+)\s+(v\d+),(v\d+|x\d+|\d+)(,(?:v\d+|x\d+|\d+))?(,v\d+)?", line)
    if not match:
        return None

    pc = hex(int(match.group(1), 16))
    opcode = match.group(3)
    vd = int(re.search(r"\d+", match.group(4)).group(0))
    op1 = int(re.search(r"\d+", match.group(5)).group(0))
    op2 = int(re.search(r"\d+", match.group(6)).group(0)) if match.group(6) else 0
    vm = 1 

    entry = {
        "opcode": opcode,
        "vd": 0,
        "rs1": 0,
        "vs1": 0,
        "vs2": 0,
        "rs2": 0,
        "rd": 0,
        "vs3": 0,
        "vm": vm,
        "imm": 0, 
    }

    flag = re.search(r'\.(.*)', opcode)
    flag = flag.group(0)
    if(flag == '.vv'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["vs1"] = op2
    elif(flag == '.vx'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["rs1"] = op2
    elif(flag == '.vi'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["imm"] = op2
    elif(flag == '.vvm'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["vs1"] = op2
        entry["vm"] = 0
    elif(flag == '.vxm'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["rs1"] = op2
        entry["vm"] = 0
    elif(flag == '.vim'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["imm"] = op2
        entry["vm"] = 0
    elif(flag == '.v.v'):
        entry["vd"] = vd
        entry["vs1"] = op1
    elif(flag == '.v.x'):
        entry["vd"] = vd
        entry["rs1"] = op1
    elif(flag == '.v.i'):
        entry["vd"] = vd
        entry["imm"] = op1
    elif(flag == '.wv'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["vs1"] = op2
    elif(flag == '.wx'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["rs1"] = op2
    elif(flag == '.wi'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["imm"] = op2
    elif(flag == '.vs'):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["vs1"] = op2

    return pc, entry

def parse_objdump_opm_line(line):
    match = re.match(r"\s*([0-9a-f]+):\s+([0-9a-f]+)\s+(\S+)\s+(v\d+),(v\d+|x\d+|\d+),(v\d+|x\d+|\d+)", line)
    if not match:
        return None

    pc = hex(int(match.group(1), 16))
    opcode = match.group(3)
    vd = int(re.search(r"\d+", match.group(4)).group(0))
    op1 = int(re.search(r"\d+", match.group(5)).group(0))
    op2 = int(re.search(r"\d+", match.group(6)).group(0))
    vm = 1 

    entry = {
        "opcode": opcode,
        "vd": 0,
        "rs1": 0,
        "vs1": 0,
        "vs2": 0,
        "rs2": 0,
        "rd": 0,
        "vs3": 0,
        "vm": vm,
        "imm": 0, 
    }

    flag = re.search(r'\.(.*)', opcode)
    flag = flag.group(0)

    if opcode in ["vmadd.vx", "vnmsub.vx", "vmacc.vx", "vnmsac.vx", "vwmaccu.vx", "vwmacc.vx", "vwmaccus.vx", "vwmaccsu.vx"]:
        entry["vd"] = vd
        entry["rs1"] = op1
        entry["vs2"] = op2
    elif opcode in ["vmadd.vv", "vnmsub.vv", "vmacc.vv", "vnmsac.vv", "vwmaccu.vv", "vwmacc.vv", "vwmaccus.vv", "vwmaccsu.vv"]:
        entry["vd"] = vd
        entry["vs1"] = op1
        entry["vs2"] = op2
    elif flag in [".vs", ".mm", ".wv", ".vm"]:
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["vs1"] = op2
    elif flag in [".vv"]:
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["vs1"] = op2
    elif flag in [".vx", ".wx"]:
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["rs1"] = op2


    return pc, entry

def parse_objdump_opf_line(line):
    match = re.match(r"\s*([0-9a-f]+):\s+([0-9a-f]+)\s+(\S+)\s+(v\d+),(v\d+|f\d+)(?:,(v\d+|f\d+))?", line)
    if not match:
        return None

    pc = hex(int(match.group(1), 16))
    opcode = match.group(3)
    vd = int(re.search(r"\d+", match.group(4)).group(0))
    op1 = int(re.search(r"\d+", match.group(5)).group(0))
    op2 = int(re.search(r"\d+", match.group(6)).group(0)) if match.group(6) else 0
    vm = 1 

    entry = {
        "opcode": opcode,
        "vd": 0,
        "rs1": 0,
        "vs1": 0,
        "vs2": 0,
        "rs2": 0,
        "rd": 0,
        "vs3": 0,
        "vm": vm,
        "imm": 0, 
    }

    flag = re.search(r'\.(.*)', opcode)
    flag = flag.group(0)

    if opcode in ["vfmadd.vf", "vfnmadd.vf", "vfmsub.vf", "vfnmsub.vf", "vfmacc.vf", "vfnmacc.vf", "vfmsac.vf", "vfnmsac.vf", "vfwmacc.vf", "vfwnmacc.vf", "vfwmsac.vf", "vfwnmsac.vf"]:
        entry["vd"] = vd
        entry["rs1"] = op1
        entry["vs2"] = op2
    elif opcode in ["vfmadd.vv", "vfnmadd.vv", "vfmsub.vv", "vfnmsub.vv", "vfmacc.vv", "vfnmacc.vv", "vfmsac.vv", "vfnmsac.vv", "vfwmacc.vv", "vfwnmacc.vv", "vfwmsac.vv", "vfwnmsac.vv"]:
        entry["vd"] = vd
        entry["vs1"] = op1
        entry["vs2"] = op2
    elif flag in (".vv", ".vs"):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["vs1"] = op2
    elif flag in (".vf"):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["rs1"] = op2
    elif flag in (".v.f"):
        entry["vd"] = vd
        entry["rs1"] = op1
    elif flag in (".vfm"):
        entry["vd"] = vd
        entry["vs2"] = op1
        entry["rs1"] = op2
        entry["vm"] = 0
    


    return pc, entry

def parse_objdump_m_line(line):
    SUPPORTED_OPCODES = {"vmsbf.m", "vmsof.m", "vmsif.m", "viota.m", "vid.m", "vfirst.m", "vcpop.m", "vmv.x.s", "vmv.s.x", "vid.v"}
    
    match = re.match(r"\s*([0-9a-f]+):\s+([0-9a-f]+)\s+(\S+)\s+(x\d+|v\d+)(,(v\d+|x\d+))?", line)
    if not match:
        return None

    pc = hex(int(match.group(1), 16))
    opcode = match.group(3)
    if opcode not in SUPPORTED_OPCODES:
        return None
    rd = int(re.search(r"\d+", match.group(4)).group(0))
    op1 = int(re.search(r"\d+", match.group(5)).group(0)) if match.group(5) else 0
    vm = 1 

    entry = {
        "opcode": opcode,
        "vd": 0,
        "rs1": 0,
        "vs1": 0,
        "vs2": 0,
        "rs2": 0,
        "rd": 0,
        "vs3": 0,
        "vm": vm,
        "imm": 0, 
    }

    if opcode in ["vmsbf.m", "vmsof.m", "vmsif.m", "viota.m", "vid.m", "vfirst.m", "vcpop.m", "vmv.x.s"]:
        entry["rd"] = rd
        entry["vs2"] = op1
    elif opcode in ["vmv.s.x"]:
        entry["vd"] = rd
        entry["rs1"] = op1
    elif opcode in ["vid.v"]:
        entry["vd"] = rd
        
    return pc, entry


def parse_objdump_file(filepath, parse_function):
    objdump_dict = {}
    with open(filepath, "r") as file:
        lines = file.readlines()
        for line in lines:
            parsed = parse_function(line)
            if parsed:
                pc, entry = parsed
                objdump_dict[pc] = entry
    return objdump_dict

def compare_dictionaries(emulator_dict, objdump_dict):
    mismatches = []
    for pc, emu_entry in emulator_dict.items():
        obj_entry = objdump_dict.get(pc)
        if not obj_entry:
            mismatches.append((pc, "Missing in objdump"))
            continue
        if emu_entry != obj_entry:
            mismatches.append((pc, emu_entry, obj_entry))
    
    for pc, obj_entry in objdump_dict.items():
        if pc not in emulator_dict:
            mismatches.append((pc, "Missing in emulator"))
    return mismatches

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare emulator output with objdump output.")
    parser.add_argument("-a", "--args", type=int, choices=range(1, 8), required=True,
                        help="Choose the parse function: 1-2=parse_objdump_line, 3=parse_objdump_opi_line, 4=parse_objdump_opm_line, 5=parse_objdump_opf_line, 6=parse_objdump_m_line.")

    args = parser.parse_args()

    # Map args to the corresponding parse functions
    parse_function_map = {
        1: parse_objdump_line,
        2: parse_objdump_line,
        3: parse_objdump_opi_line,
        4: parse_objdump_opm_line,
        5: parse_objdump_opf_line,
        6: parse_objdump_m_line,
    }

    parse_function = parse_function_map[args.args]

    emulator_filepath = "test_emu.txt"
    objdump_filepath = "test.txt"

    emulator_dict = parse_emulator_file(emulator_filepath)
    objdump_dict = parse_objdump_file(objdump_filepath, parse_function)

    print(f"\ntest case: {len(emulator_dict)}\t {len(objdump_dict)}\n")
    mismatches = compare_dictionaries(emulator_dict, objdump_dict)

    if mismatches:
        print("\nMismatches found:\n")
        for mismatch in mismatches:
            print(mismatch)
            # print(f"{mismatch[0]}\n{mismatch[1]}\n{mismatch[2]}")
        assert False, f"Mismatches detected: {len(mismatches)} issues found."
    else:
        print("\nAll lines match.\n")