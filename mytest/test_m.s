# This file has been automatically generated by the script.
# Test case for Vectore load instructions.
.section .text
.global main
main:
    vmv.s.x v29, x4
    vmv.s.x v8, x8
    vmv.s.x v1, x14
    vmv.s.x v17, x5
    vmv.s.x v21, x10
    vmv.s.x v6, x18
    vmv.s.x v23, x9
    vmv.s.x v11, x9
    vmv.s.x v28, x22
    vmv.s.x v28, x8
    vmv.s.x v22, x13
    vmv.s.x v25, x12
    vmv.s.x v14, x11
    vmv.s.x v15, x0
    vmv.s.x v22, x20
    vmv.x.s x18, v3
    vmv.x.s x31, v28
    vmv.x.s x22, v23
    vmv.x.s x11, v16
    vmv.x.s x0, v16
    vmv.x.s x1, v3
    vmv.x.s x28, v12
    vmv.x.s x28, v4
    vmv.x.s x3, v26
    vmv.x.s x12, v21
    vmv.x.s x3, v14
    vmv.x.s x14, v1
    vmv.x.s x23, v28
    vmv.x.s x30, v15
    vmv.x.s x20, v0
    vcpop.m x27, v26
    vcpop.m x22, v21
    vcpop.m x8, v7
    vcpop.m x14, v14
    vcpop.m x6, v17
    vcpop.m x31, v13
    vcpop.m x21, v2
    vcpop.m x31, v7
    vcpop.m x20, v21
    vcpop.m x7, v3
    vcpop.m x19, v28
    vcpop.m x27, v25
    vcpop.m x14, v24
    vcpop.m x12, v7
    vcpop.m x11, v24
    vfirst.m x9, v21
    vfirst.m x5, v9
    vfirst.m x20, v11
    vfirst.m x28, v24
    vfirst.m x12, v12
    vfirst.m x16, v22
    vfirst.m x2, v0
    vfirst.m x11, v10
    vfirst.m x9, v5
    vfirst.m x8, v13
    vfirst.m x24, v18
    vfirst.m x10, v9
    vfirst.m x3, v19
    vfirst.m x10, v14
    vfirst.m x28, v25
    vmsbf.m v8, v14
    vmsbf.m v24, v11
    vmsbf.m v5, v15
    vmsbf.m v16, v19
    vmsbf.m v26, v7
    vmsbf.m v13, v23
    vmsbf.m v4, v21
    vmsbf.m v21, v17
    vmsbf.m v5, v30
    vmsbf.m v25, v5
    vmsbf.m v21, v21
    vmsbf.m v16, v16
    vmsbf.m v11, v25
    vmsbf.m v0, v30
    vmsbf.m v17, v10
    vmsof.m v30, v31
    vmsof.m v13, v25
    vmsof.m v14, v8
    vmsof.m v24, v18
    vmsof.m v25, v5
    vmsof.m v15, v10
    vmsof.m v31, v25
    vmsof.m v14, v17
    vmsof.m v18, v16
    vmsof.m v31, v27
    vmsof.m v13, v20
    vmsof.m v16, v29
    vmsof.m v7, v11
    vmsof.m v27, v0
    vmsof.m v21, v4
    vmsif.m v29, v8
    vmsif.m v29, v5
    vmsif.m v25, v10
    vmsif.m v4, v30
    vmsif.m v11, v1
    vmsif.m v25, v2
    vmsif.m v1, v25
    vmsif.m v1, v9
    vmsif.m v29, v11
    vmsif.m v4, v21
    vmsif.m v16, v22
    vmsif.m v29, v29
    vmsif.m v31, v7
    vmsif.m v30, v15
    vmsif.m v2, v13
    viota.m v17, v31
    viota.m v13, v11
    viota.m v0, v10
    viota.m v9, v2
    viota.m v0, v15
    viota.m v28, v6
    viota.m v21, v10
    viota.m v30, v16
    viota.m v18, v10
    viota.m v2, v16
    viota.m v31, v13
    viota.m v28, v30
    viota.m v3, v1
    viota.m v27, v10
    viota.m v0, v20
    vid.v v27
    vid.v v5
    vid.v v13
    vid.v v31
    vid.v v15
    vid.v v19
    vid.v v29
    vid.v v15
    vid.v v17
    vid.v v0
    vid.v v17
    vid.v v12
    vid.v v30
    vid.v v13
    vid.v v3
    li a7, 10
    ecall