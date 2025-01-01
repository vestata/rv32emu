import random
import argparse

nf = (2, 3, 4, 5, 6, 7, 8)
eew = (8, 16, 32, 64)

vload = [
    "vle8.v",
    "vle16.v",
    "vle32.v",
    "vle64.v",
    "vlseg2e8.v",
    "vlseg3e8.v",
    "vlseg4e8.v",
    "vlseg5e8.v",
    "vlseg6e8.v",
    "vlseg7e8.v",
    "vlseg8e8.v",
    "vlseg2e16.v",
    "vlseg3e16.v",
    "vlseg4e16.v",
    "vlseg5e16.v",
    "vlseg6e16.v",
    "vlseg7e16.v",
    "vlseg8e16.v",
    "vlseg2e32.v",
    "vlseg3e32.v",
    "vlseg4e32.v",
    "vlseg5e32.v",
    "vlseg6e32.v",
    "vlseg7e32.v",
    "vlseg8e32.v",
    "vlseg2e64.v",
    "vlseg3e64.v",
    "vlseg4e64.v",
    "vlseg5e64.v",
    "vlseg6e64.v",
    "vlseg7e64.v",
    "vlseg8e64.v",
    "vl1re8.v",
    "vl2re8.v",
    "vl4re8.v",
    "vl8re8.v",
    "vl1re16.v",
    "vl2re16.v",
    "vl4re16.v",
    "vl8re16.v",
    "vl1re32.v",
    "vl2re32.v",
    "vl4re32.v",
    "vl8re32.v",
    "vl1re64.v",
    "vl2re64.v",
    "vl4re64.v",
    "vl8re64.v",
    "vlm.v",
    "vle8ff.v",
    "vle16ff.v",
    "vle32ff.v",
    "vle64ff.v",
    "vlseg2e8ff.v",
    "vlseg3e8ff.v",
    "vlseg4e8ff.v",
    "vlseg5e8ff.v",
    "vlseg6e8ff.v",
    "vlseg7e8ff.v",
    "vlseg8e8ff.v",
    "vlseg2e16ff.v",
    "vlseg3e16ff.v",
    "vlseg4e16ff.v",
    "vlseg5e16ff.v",
    "vlseg6e16ff.v",
    "vlseg7e16ff.v",
    "vlseg8e16ff.v",
    "vlseg2e32ff.v",
    "vlseg3e32ff.v",
    "vlseg4e32ff.v",
    "vlseg5e32ff.v",
    "vlseg6e32ff.v",
    "vlseg7e32ff.v",
    "vlseg8e32ff.v",
    "vlseg2e64ff.v",
    "vlseg3e64ff.v",
    "vlseg4e64ff.v",
    "vlseg5e64ff.v",
    "vlseg6e64ff.v",
    "vlseg7e64ff.v",
    "vlseg8e64ff.v",
    "vluxei8.v",
    "vluxei16.v",
    "vluxei32.v",
    "vluxei64.v",
    "vluxseg2ei8.v",
    "vluxseg3ei8.v",
    "vluxseg4ei8.v",
    "vluxseg5ei8.v",
    "vluxseg6ei8.v",
    "vluxseg7ei8.v",
    "vluxseg8ei8.v",
    "vluxseg2ei16.v",
    "vluxseg3ei16.v",
    "vluxseg4ei16.v",
    "vluxseg5ei16.v",
    "vluxseg6ei16.v",
    "vluxseg7ei16.v",
    "vluxseg8ei16.v",
    "vluxseg2ei32.v",
    "vluxseg3ei32.v",
    "vluxseg4ei32.v",
    "vluxseg5ei32.v",
    "vluxseg6ei32.v",
    "vluxseg7ei32.v",
    "vluxseg8ei32.v",
    "vluxseg2ei64.v",
    "vluxseg3ei64.v",
    "vluxseg4ei64.v",
    "vluxseg5ei64.v",
    "vluxseg6ei64.v",
    "vluxseg7ei64.v",
    "vluxseg8ei64.v",
    "vlse8.v",
    "vlse16.v",
    "vlse32.v",
    "vlse64.v",
    "vlsseg2e8.v",
    "vlsseg3e8.v",
    "vlsseg4e8.v",
    "vlsseg5e8.v",
    "vlsseg6e8.v",
    "vlsseg7e8.v",
    "vlsseg8e8.v",
    "vlsseg2e16.v",
    "vlsseg3e16.v",
    "vlsseg4e16.v",
    "vlsseg5e16.v",
    "vlsseg6e16.v",
    "vlsseg7e16.v",
    "vlsseg8e16.v",
    "vlsseg2e32.v",
    "vlsseg3e32.v",
    "vlsseg4e32.v",
    "vlsseg5e32.v",
    "vlsseg6e32.v",
    "vlsseg7e32.v",
    "vlsseg8e32.v",
    "vlsseg2e64.v",
    "vlsseg3e64.v",
    "vlsseg4e64.v",
    "vlsseg5e64.v",
    "vlsseg6e64.v",
    "vlsseg7e64.v",
    "vlsseg8e64.v",
    "vloxei8.v",
    "vloxei16.v",
    "vloxei32.v",
    "vloxei64.v",
    "vloxseg2ei8.v",
    "vloxseg3ei8.v",
    "vloxseg4ei8.v",
    "vloxseg5ei8.v",
    "vloxseg6ei8.v",
    "vloxseg7ei8.v",
    "vloxseg8ei8.v",
    "vloxseg2ei16.v",
    "vloxseg3ei16.v",
    "vloxseg4ei16.v",
    "vloxseg5ei16.v",
    "vloxseg6ei16.v",
    "vloxseg7ei16.v",
    "vloxseg8ei16.v",
    "vloxseg2ei32.v",
    "vloxseg3ei32.v",
    "vloxseg4ei32.v",
    "vloxseg5ei32.v",
    "vloxseg6ei32.v",
    "vloxseg7ei32.v",
    "vloxseg8ei32.v",
    "vloxseg2ei64.v",
    "vloxseg3ei64.v",
    "vloxseg4ei64.v",
    "vloxseg5ei64.v",
    "vloxseg6ei64.v",
    "vloxseg7ei64.v",
    "vloxseg8ei64.v",
]

def generate_vector_load_insn(test_program, count = 1):
    # VL
    insn_vd_rs1 = []
    for _ in ("", "ff"):
        for i in eew:
            insn_vd_rs1.append(f"vle{i}{_}.v")
        for i in eew:
            for j in nf:
                insn_vd_rs1.append(f"vlseg{j}e{i}{_}.v")
    for i in eew:
        for j in (1, 2, 4, 8):
            insn_vd_rs1.append(f"vl{j}re{i}.v")
    insn_vd_rs1.append("vlm.v")
    # VLS
    insn_vd_rs1_rs2 = []
    for i in eew:
        insn_vd_rs1_rs2.append(f"vlse{i}.v")
    for i in eew:
        for j in nf:
            insn_vd_rs1_rs2.append(f"vlsseg{j}e{i}.v")
    # VLX
    insn_vd_rs1_vs2 = []
    for i in eew:
        insn_vd_rs1_vs2.append(f"vluxei{i}.v")
    for i in eew:
        for j in nf:
            insn_vd_rs1_vs2.append(f"vluxseg{j}ei{i}.v")
    for i in eew:
        insn_vd_rs1_vs2.append(f"vloxei{i}.v")
    for i in eew:
        for j in nf:
            insn_vd_rs1_vs2.append(f"vloxseg{j}ei{i}.v")
    
    # Add vd, (rs1) instructions
    for instr in insn_vd_rs1:
        for vd in range(count):
            for rs1 in range(count):
                test_program.append(f"    {instr} v{random.randint(0, 31)}, (x{random.randint(0, 31)})")

    # Add vd, (rs1), vs2 instructions
    for instr in insn_vd_rs1_rs2:
        for vd in range(count):
            for rs1 in range(count):
                for rs2 in range(count):
                    test_program.append(f"    {instr} v{random.randint(0, 31)}, (x{random.randint(0, 31)}), x{random.randint(0, 31)}")

    # Add vd, (rs1), rs2 instructions
    for instr in insn_vd_rs1_vs2:
        for vd in range(count):
            for rs1 in range(count):
                for vs2 in range(count):
                    test_program.append(f"    {instr} v{random.randint(0, 31)}, (x{random.randint(0, 31)}), v{random.randint(0, 31)}")
    
vstore = [
    "vse8.v",
    "vse16.v",
    "vse32.v",
    "vse64.v",
    "vsseg2e8.v",
    "vsseg3e8.v",
    "vsseg4e8.v",
    "vsseg5e8.v",
    "vsseg6e8.v",
    "vsseg7e8.v",
    "vsseg8e8.v",
    "vsseg2e16.v",
    "vsseg3e16.v",
    "vsseg4e16.v",
    "vsseg5e16.v",
    "vsseg6e16.v",
    "vsseg7e16.v",
    "vsseg8e16.v",
    "vsseg2e32.v",
    "vsseg3e32.v",
    "vsseg4e32.v",
    "vsseg5e32.v",
    "vsseg6e32.v",
    "vsseg7e32.v",
    "vsseg8e32.v",
    "vsseg2e64.v",
    "vsseg3e64.v",
    "vsseg4e64.v",
    "vsseg5e64.v",
    "vsseg6e64.v",
    "vsseg7e64.v",
    "vsseg8e64.v",
    "vs1r.v",
    "vs2r.v",
    "vs4r.v",
    "vs8r.v",
    "vsm.v",
    "vsuxei8.v",
    "vsuxei16.v",
    "vsuxei32.v",
    "vsuxei64.v",
    "vsuxseg2ei8.v",
    "vsuxseg3ei8.v",
    "vsuxseg4ei8.v",
    "vsuxseg5ei8.v",
    "vsuxseg6ei8.v",
    "vsuxseg7ei8.v",
    "vsuxseg8ei8.v",
    "vsuxseg2ei16.v",
    "vsuxseg3ei16.v",
    "vsuxseg4ei16.v",
    "vsuxseg5ei16.v",
    "vsuxseg6ei16.v",
    "vsuxseg7ei16.v",
    "vsuxseg8ei16.v",
    "vsuxseg2ei32.v",
    "vsuxseg3ei32.v",
    "vsuxseg4ei32.v",
    "vsuxseg5ei32.v",
    "vsuxseg6ei32.v",
    "vsuxseg7ei32.v",
    "vsuxseg8ei32.v",
    "vsuxseg2ei64.v",
    "vsuxseg3ei64.v",
    "vsuxseg4ei64.v",
    "vsuxseg5ei64.v",
    "vsuxseg6ei64.v",
    "vsuxseg7ei64.v",
    "vsuxseg8ei64.v",
    "vsse8.v",
    "vsse16.v",
    "vsse32.v",
    "vsse64.v",
    "vssseg2e8.v",
    "vssseg3e8.v",
    "vssseg4e8.v",
    "vssseg5e8.v",
    "vssseg6e8.v",
    "vssseg7e8.v",
    "vssseg8e8.v",
    "vssseg2e16.v",
    "vssseg3e16.v",
    "vssseg4e16.v",
    "vssseg5e16.v",
    "vssseg6e16.v",
    "vssseg7e16.v",
    "vssseg8e16.v",
    "vssseg2e32.v",
    "vssseg3e32.v",
    "vssseg4e32.v",
    "vssseg5e32.v",
    "vssseg6e32.v",
    "vssseg7e32.v",
    "vssseg8e32.v",
    "vssseg2e64.v",
    "vssseg3e64.v",
    "vssseg4e64.v",
    "vssseg5e64.v",
    "vssseg6e64.v",
    "vssseg7e64.v",
    "vssseg8e64.v",
    "vsoxei8.v",
    "vsoxei16.v",
    "vsoxei32.v",
    "vsoxei64.v",
    "vsoxseg2ei8.v",
    "vsoxseg3ei8.v",
    "vsoxseg4ei8.v",
    "vsoxseg5ei8.v",
    "vsoxseg6ei8.v",
    "vsoxseg7ei8.v",
    "vsoxseg8ei8.v",
    "vsoxseg2ei16.v",
    "vsoxseg3ei16.v",
    "vsoxseg4ei16.v",
    "vsoxseg5ei16.v",
    "vsoxseg6ei16.v",
    "vsoxseg7ei16.v",
    "vsoxseg8ei16.v",
    "vsoxseg2ei32.v",
    "vsoxseg3ei32.v",
    "vsoxseg4ei32.v",
    "vsoxseg5ei32.v",
    "vsoxseg6ei32.v",
    "vsoxseg7ei32.v",
    "vsoxseg8ei32.v",
    "vsoxseg2ei64.v",
    "vsoxseg3ei64.v",
    "vsoxseg4ei64.v",
    "vsoxseg5ei64.v",
    "vsoxseg6ei64.v",
    "vsoxseg7ei64.v",
    "vsoxseg8ei64.v",
]


def generate_vector_store_insn(test_program, count = 1):
    # VS
    insn_vs3_rs1 = []
    
    for i in eew:
        insn_vs3_rs1.append(f"vse{i}.v")
    for i in eew:
        for j in nf:
            insn_vs3_rs1.append(f"vsseg{j}e{i}.v")
    for i in (1, 2, 4, 8):
        insn_vs3_rs1.append(f"vs{i}r.v")
    insn_vs3_rs1.append("vsm.v")
    # VSS
    insn_vs3_rs1_rs2 = []
    for i in eew:
        insn_vs3_rs1_rs2.append(f"vsse{i}.v")
    for i in eew:
        for j in nf:
            insn_vs3_rs1_rs2.append(f"vssseg{j}e{i}.v")
    # VSX
    insn_vs3_rs1_vs2 = []
    for i in eew:
        insn_vs3_rs1_vs2.append(f"vsuxei{i}.v")
    for i in eew:
        for j in nf:
            insn_vs3_rs1_vs2.append(f"vsuxseg{j}ei{i}.v")
    for i in eew:
        insn_vs3_rs1_vs2.append(f"vsoxei{i}.v")
    for i in eew:
        for j in nf:
            insn_vs3_rs1_vs2.append(f"vsoxseg{j}ei{i}.v")
    
    # Add vd, (rs1) instructions
    for instr in insn_vs3_rs1:
        for vd in range(count):
            for rs1 in range(count):
                test_program.append(f"    {instr} v{random.randint(0, 31)}, (x{random.randint(0, 31)})")

    # Add vd, (rs1), vs2 instructions
    for instr in insn_vs3_rs1_rs2:
        for vd in range(count):
            for rs1 in range(count):
                for rs2 in range(count):
                    test_program.append(f"    {instr} v{random.randint(0, 31)}, (x{random.randint(0, 31)}), x{random.randint(0, 31)}")

    # Add vd, (rs1), rs2 instructions
    for instr in insn_vs3_rs1_vs2:
        for vd in range(count):
            for rs1 in range(count):
                for vs2 in range(count):
                    test_program.append(f"    {instr} v{random.randint(0, 31)}, (x{random.randint(0, 31)}), v{random.randint(0, 31)}")
    

def generate_opi_insn(test_program, count = 1):
    # opivv = ['vadd.vv', 'vsub.vv', 'vadc.vvm', 'vmadc.vvm', 'vmadc.vv', 'vsbc.vvm', 'vmsbc.vvm', 'vmsbc.vv', 'vand.vv', 'vor.vv', 'vxor.vv', 'vsll.vv', 'vsrl.vv', 'vsra.vv', 'vnsrl.wv', 'vnsra.wv', 'vmseq.vv', 'vmsne.vv', 'vmsltu.vv', 'vmslt.vv', 'vmsleu.vv', 'vmsle.vv', ]
    # opfvv = []
    # opmvv = ['vwaddu.vv', 'vwsubu.vv', 'vwadd.vv', 'vwsub.vv', 'vwaddu.wv', 'vwsubu.wv', 'vwadd.wv', 'vwsub.wv', ]
    # opivi = ['vadd.vi', 'vsub.vi', 'vrsub.vi', 'vadc.vim', 'vmadc.vim', 'vmadc.vi', 'vand.vi', 'vor.vi', 'vxor.vi', 'vsll.vi', 'vsrl.vi', 'vsra.vi', 'vnsrl.wi', 'vnsra.wi', 'vmseq.vi', 'vmsne.vi', 'vmsleu.vi', 'vmsle.vi', 'vmsgtu.vi', 'vmsgt.vi', ]
    # opivx = ['vadd.vx', 'vrsub.vx', 'vadc.vxm', 'vmadc.vxm', 'vmadc.vx', 'vsbc.vxm', 'vmsbc.vxm', 'vmsbc.vx', 'vand.vx', 'vor.vx', 'vxor.vx', 'vsll.vx', 'vsrl.vx', 'vsra.vx', 'vnsrl.wx', 'vnsra.wx', 'vmseq.vx', 'vmsne.vx', 'vmsltu.vx', 'vmslt.vx', 'vmsleu.vx', 'vmsle.vx', 'vmsgtu.vx', 'vmsgt.vx', ]
    # opfvf = []
    # opmvx = ['vwaddu.vx', 'vwsubu.vx', 'vwadd.vx', 'vwsub.vx', 'vwaddu.wx', 'vwsubu.wx', 'vwadd.wx', 'vwsub.wx']
    
    # # 0-31
    # uimm = ['vsll', 'vsrl', 'vsra', 'vnsrl', 'vnsra']
    
    # # -16~15: vmsle
    # # -15~16: vmslt, vmseg
    # # 0~15: vmsleu
    # # 1~16: vmsltu, vmsgeu
    # '''
    # Stopped at spec page 51
    # '''

    instructions = [
    "vadd.vv",
    "vadd.vx",
    "vadd.vi",
    "vsub.vv",
    "vsub.vx",
    "vrsub.vx",
    "vrsub.vi",
    "vminu.vv",
    "vminu.vx",
    "vmin.vv",
    "vmin.vx",
    "vmaxu.vv",
    "vmaxu.vx",
    "vmax.vv",
    "vmax.vx",
    "vand.vv",
    "vand.vx",
    "vand.vi",
    "vor.vv",
    "vor.vx",
    "vor.vi",
    "vxor.vv",
    "vxor.vx",
    "vxor.vi",
    "vrgather.vv",
    "vrgather.vx",
    "vrgather.vi",
    "vslideup.vx",
    "vslideup.vi",
    "vrgatherei16.vv",
    "vslidedown.vx",
    "vslidedown.vi",
    "vadc.vvm",
    "vadc.vxm",
    "vadc.vim",
    "vmadc.vv",
    "vmadc.vx",
    "vmadc.vi",
    "vsbc.vvm",
    "vsbc.vxm",
    "vmsbc.vv",
    "vmsbc.vx",
    "vmerge.vvm",
    "vmerge.vxm",
    "vmerge.vim",
    "vmv.v.v",
    "vmv.v.x",
    "vmv.v.i",
    "vmseq.vv",
    "vmseq.vx",
    "vmseq.vi",
    "vmsne.vv",
    "vmsne.vx",
    "vmsne.vi",
    "vmsltu.vv",
    "vmsltu.vx",
    "vmslt.vv",
    "vmslt.vx",
    "vmsleu.vv",
    "vmsleu.vx",
    "vmsleu.vi",
    "vmsle.vv",
    "vmsle.vx",
    "vmsle.vi",
    "vmsgtu.vx",
    "vmsgtu.vi",
    "vmsgt.vx",
    "vmsgt.vi",
    "vsaddu.vv",
    "vsaddu.vx",
    "vsaddu.vi",
    "vsadd.vv",
    "vsadd.vx",
    "vsadd.vi",
    "vssubu.vv",
    "vssubu.vx",
    "vssub.vv",
    "vssub.vx",
    "vsll.vv",
    "vsll.vx",
    "vsll.vi",
    "vsmul.vv",
    "vsmul.vx",
    "vsrl.vv",
    "vsrl.vx",
    "vsrl.vi",
    "vsra.vv",
    "vsra.vx",
    "vsra.vi",
    "vssrl.vv",
    "vssrl.vx",
    "vssrl.vi",
    "vssra.vv",
    "vssra.vx",
    "vssra.vi",
    "vnsrl.wv",
    "vnsrl.wx",
    "vnsrl.wi",
    "vnsra.wv",
    "vnsra.wx",
    "vnsra.wi",
    "vnclipu.wv",
    "vnclipu.wx",
    "vnclipu.wi",
    "vnclip.wv",
    "vnclip.wx",
    "vnclip.wi",
    "vwredsumu.vs",
    "vwredsum.vs"
]
    
    for instr in instructions:
        for _ in range(count):
            if instr.endswith(".vv"):
                # instr.vv vd, vs2, vs1
                # vd  = 2
                # vs2 = 3
                # vs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, v{vs1}")

            elif instr.endswith(".vx"):
                # instr.vx vd, vs2, rs1 (xN)
                # vd  = 2
                # vs2 = 3
                # rs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                rs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, x{rs1}")

            elif instr.endswith(".vi"):
                # instr.vi vd, vs2, imm
                # vd  = 2
                # vs2 = 3
                imm = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                # imm = random.randint(-16, 15)  # 5-bit signed immediate
                test_program.append(f"    {instr} v{vd}, v{vs2}, {imm}")

            elif instr.endswith(".vvm"):
                # instr.vvm vd, vs2, vs1 
                # vd  = 2
                # vs2 = 3
                # vs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                # v0  mask
                test_program.append(f"    {instr} v{vd}, v{vs2}, v{vs1}, v0")

            elif instr.endswith(".vxm"):
                # instr.vxm vd, vs2, rs1, (mask)
                # vd  = 2
                # vs2 = 3
                # rs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                rs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, x{rs1}, v0")

            elif instr.endswith(".vim"):
                #  instr.vim vd, vs2, imm, (mask)
                # vd  = 2
                # vs2 = 3
                imm = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                # imm = random.randint(-16, 15)
                test_program.append(f"    {instr} v{vd}, v{vs2}, {imm}, v0")
                
            elif instr.endswith(".v.v"):
                # vmv.v.v vd, vs1
                # vd  = 2
                # vs1 = 3
                vd  = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs1}")

            elif instr.endswith(".v.x"):
                # vmv.v.x vd, rs1
                # vd  = 2
                # rs1 = 3
                vd  = random.randint(0, 31)
                rs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, x{rs1}")

            elif instr.endswith(".v.i"):
                # vmv.v.i vd, imm
                # vd  = 2
                imm = 3
                vd  = random.randint(0, 31)
                # imm = random.randint(-16, 15)
                test_program.append(f"    {instr} v{vd}, {imm}")

            elif instr.endswith(".wv"):
                # instr.vv vd, vs2, vs1
                # vd  = 2
                # vs2 = 3
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, v{vs1}")

            elif instr.endswith(".wx"):
                # instr.vx vd, vs2, rs1 (xN)
                # vd  = 2
                # vs2 = 3
                # rs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                rs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, x{rs1}")

            elif instr.endswith(".wi"):
                # instr.vi vd, vs2, imm
                # vd  = 2
                # vs2 = 3
                imm = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                # imm = random.randint(-16, 15)  # 5-bit signed immediate
                test_program.append(f"    {instr} v{vd}, v{vs2}, {imm}")

            elif instr.endswith(".vs"):
                # instr.vv vd, vs2, vs1
                # vd  = 2
                # vs2 = 3
                # vs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, v{vs1}")


def generate_opm_insn(test_program, count = 1):
    opm_insn = [
        "vredsum.vs",
        "vredand.vs",
        "vredor.vs",
        "vredxor.vs",
        "vredminu.vs",
        "vredmin.vs",
        "vredmaxu.vs",
        "vredmax.vs",
        "vaaddu.vv",
        "vaaddu.vx",
        "vaadd.vv",
        "vaadd.vx",
        "vasubu.vv",
        "vasubu.vx",
        "vasub.vv",
        "vasub.vx",
        "vslide1up.vx",
        "vslide1down.vx",
        "vcompress.vm",
        "vmandn.mm",
        "vmand.mm",
        "vmor.mm",
        "vmxor.mm",
        "vmorn.mm",
        "vmnand.mm",
        "vmnor.mm",
        "vmxnor.mm",
        "vdivu.vv",
        "vdivu.vx",
        "vdiv.vv",
        "vdiv.vx",
        "vremu.vv",
        "vremu.vx",
        "vrem.vv",
        "vrem.vx",
        "vmulhu.vv",
        "vmulhu.vx",
        "vmul.vv",
        "vmul.vx",
        "vmulhsu.vv",
        "vmulhsu.vx",
        "vmulh.vv",
        "vmulh.vx",
        "vmadd.vv",
        "vmadd.vx",
        "vnmsub.vv",
        "vnmsub.vx",
        "vmacc.vv",
        "vmacc.vx",
        "vnmsac.vv",
        "vnmsac.vx",
        "vwaddu.vv",
        "vwaddu.vx",
        "vwadd.vv",
        "vwadd.vx",
        "vwsubu.vv",
        "vwsubu.vx",
        "vwsub.vv",
        "vwsub.vx",
        "vwaddu.wv",
        "vwaddu.wx",
        "vwadd.wv",
        "vwadd.wx",
        "vwsubu.wv",
        "vwsubu.wx",
        "vwsub.wv",
        "vwsub.wx",
        "vwmulu.vv",
        "vwmulu.vx",
        "vwmulsu.vv",
        "vwmulsu.vx",
        "vwmul.vv",
        "vwmul.vx",
        "vwmaccu.vv",
        "vwmaccu.vx",
        "vwmacc.vv",
        "vwmacc.vx",
        "vwmaccus.vx",
        "vwmaccsu.vv",
        "vwmaccsu.vx"
    ]

    for instr in opm_insn:
        for _ in range(count):
            if instr in ["vmadd.vx", "vnmsub.vx", "vmacc.vx", "vnmsac.vx", "vwmaccu.vx", "vwmacc.vx", "vwmaccus.vx", "vwmaccsu.vx"]:
                # vop vd, rs1, vs2, vm
                # vd  = 2
                # vs2 = 3
                # rs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, x{rs1}, v{vs2}")
                
            elif instr in ["vmadd.vv", "vnmsub.vv", "vmacc.vv", "vnmsac.vv", "vwmaccu.vv", "vwmacc.vv", "vwmaccus.vv", "vwmaccsu.vv"]:
                # vop vd, rs1, vs2, vm
                # vd  = 2
                # vs1 = 3
                # vs2 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs1}, v{vs2}")
                
            elif instr.endswith((".vs", ".mm")):
                # vop.vs vd, vs2, vs1, vm
                # vd  = 2
                # vs2 = 3
                # vs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, v{vs1}")
    
            elif instr.endswith(".vv"):
                # instr.vv vd, vs2, vs1
                # vd  = 2
                # vs2 = 3
                # vs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, v{vs1}")

            elif instr.endswith(".vx"):
                # instr.vx vd, vs2 , rs1
                # vd  = 2
                # vs2 = 3
                # rs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                rs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, x{rs1}")
            
            elif instr.endswith(".wv"):
                # instr.vv vd, vs2, vs1
                # vd  = 2
                # vs2 = 3
                # vs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, v{vs1}")
            
            elif instr.endswith(".wx"):
                # instr.vx vd, vs2, rs1 
                # vd  = 2
                # vs2 = 3
                # rs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                rs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, x{rs1}")

            elif instr.endswith(".vm"):
                # instr.vx vd, vs2, rs1
                # vd  = 2
                # vs2 = 3
                # rs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                rs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, v{rs1}")

        
def generate_opf_insn(test_program, count = 1):
    opf_insn = [
        "vfadd.vv",
        "vfadd.vf",
        "vfredusum.vs",
        "vfsub.vv",
        "vfsub.vf",
        "vfredosum.vs",
        "vfmin.vv",
        "vfmin.vf",
        "vfredmin.vs",
        "vfmax.vv",
        "vfmax.vf",
        "vfredmax.vs",
        "vfsgnj.vv",
        "vfsgnj.vf",
        "vfsgnjn.vv",
        "vfsgnjn.vf",
        "vfsgnjx.vv",
        "vfsgnjx.vf",
        "vfslide1up.vf",
        "vfslide1down.vf",
        "vfmerge.vfm",
        "vfmv.v.f",
        "vmfeq.vv",
        "vmfeq.vf",
        "vmfle.vv",
        "vmfle.vf",
        "vmflt.vv",
        "vmflt.vf",
        "vmfne.vv",
        "vmfne.vf",
        "vmfgt.vf",
        "vmfge.vf",
        "vfdiv.vv",
        "vfdiv.vf",
        "vfrdiv.vf",
        "vfmul.vv",
        "vfmul.vf",
        "vfrsub.vf",
        "vfmadd.vv",
        "vfmadd.vf",
        "vfnmadd.vv",
        "vfnmadd.vf",
        "vfmsub.vv",
        "vfmsub.vf",
        "vfnmsub.vv",
        "vfnmsub.vf",
        "vfmacc.vv",
        "vfmacc.vf",
        "vfnmacc.vv",
        "vfnmacc.vf",
        "vfmsac.vv",
        "vfmsac.vf",
        "vfnmsac.vv",
        "vfnmsac.vf",
        "vfwadd.vv",
        "vfwadd.vf",
        "vfwredusum.vs",
        "vfwsub.vv",
        "vfwsub.vf",
        "vfwredosum.vs",
        "vfwadd.wv",
        "vfwadd.wf",
        "vfwsub.wv",
        "vfwsub.wf",
        "vfwmul.vv",
        "vfwmul.vf",
        "vfwmacc.vv",
        "vfwmacc.vf",
        "vfwnmacc.vv",
        "vfwnmacc.vf",
        "vfwmsac.vv",
        "vfwmsac.vf",
        "vfwnmsac.vv",
        "vfwnmsac.vf"
    ]

    for instr in opf_insn:
        for _ in range(count):
            if instr in ["vfmadd.vf", "vfnmadd.vf", "vfmsub.vf", "vfnmsub.vf", "vfmacc.vf", "vfnmacc.vf", "vfmsac.vf", "vfnmsac.vf", "vfwmacc.vf", "vfwnmacc.vf", "vfwmsac.vf", "vfwnmsac.vf"]:
                # vop.vv vd, vs2, vs1, vm
                # vd  = 2
                # rs1 = 3
                # vs2 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, f{rs1}, v{vs2}")
                
            elif instr.endswith((".vv", ".vs")):
                # vop.vv vd, vs2, vs1, vm
                # vd  = 2
                # vs2 = 3
                # vs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, v{vs1}")
            
            elif instr.endswith(".vf"):
                # instr.vx vd, vs2 , rs1
                # vd  = 2
                # vs2 = 3
                # rs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                rs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, f{rs1}")
            
            elif instr.endswith(".v.f"):
                # vmv.v.v vd, vs1
                # vd  = 2
                # rs1 = 3
                vd  = random.randint(0, 31)
                vs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, f{rs1}")
            
            elif instr.endswith(".vfm"):
                # instr.vx vd, vs2 , rs1
                # vd  = 2
                # vs2 = 3
                # rs1 = 8
                vd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                rs1 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, v{vs2}, f{rs1}, v0")
            


def generate_m_insn(test_program, count = 1):
    m_insn = [
        "vmv.s.x",
        "vmv.x.s",
        "vcpop.m",
        "vfirst.m",
        "vmsbf.m",
        "vmsof.m",
        "vmsif.m",
        "viota.m",
        "vid.v"
    ]

    for instr in m_insn:
        for _ in range(count):
            if instr in ["vmsbf.m", "vmsof.m", "vmsif.m", "viota.m", "vid.m"]:
                # vop.m vd, vs2, vm
                # vd  = 2
                # vs2 = 8
                rd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                test_program.append(f"    {instr} v{rd}, v{vs2}")
            elif instr in ["vmv.s.x"]:
                # vop.m vd, rs2, vm
                # vd  = 2
                # rs2 = 8
                vd  = random.randint(0, 31)
                rs2 = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}, x{rs2}")
            elif instr in ["vid.v"]:
                # vop.m vd, rs2, vm
                # vd  = 2
                vd  = random.randint(0, 31)
                test_program.append(f"    {instr} v{vd}")
            else:
                # vop.m rd, vs2, vm
                # rd  = 2
                # vs2 = 8
                rd  = random.randint(0, 31)
                vs2 = random.randint(0, 31)
                test_program.append(f"    {instr} x{rd}, v{vs2}")
                

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate RISC-V test cases.")
    parser.add_argument("-g", "--generate", type=int, choices=range(1, 7),
                        help="Choose which instructions to generate: 1=vector_load, 2=vector_store, 3=opi, 4=opm, 5=opf, 6=m")

    args = parser.parse_args()
    
    test_program = [
        "# This file has been automatically generated by the script.",
        "# Test case for Vectore load instructions.",
        ".section .text",
        ".global main",
        "main:"
    ]

    flag = args.generate
    iter = 15
    
    if flag == 1:
        generate_vector_load_insn(test_program, iter)
    elif flag == 2:
        generate_vector_store_insn(test_program, iter)
    elif flag == 3:
        generate_opi_insn(test_program, iter)
    elif flag == 4:
        generate_opm_insn(test_program, iter)
    elif flag == 5:
        generate_opf_insn(test_program, iter)
    elif flag == 6:
        generate_m_insn(test_program, iter)

    test_program.append("    li a7, 10")
    test_program.append("    ecall")
    
    with open("test.s", "w") as f:
        f.write("\n".join(test_program))
