/*
 * rv32emu is freely redistributable under the MIT License. See the file
 * "LICENSE" for information on usage and redistribution of this file.
 */

#pragma once

#include <stdint.h>

#include "riscv.h"

/* clang-format off */
enum {
    //                    ....xxxx....xxxx....xxxx....xxxx
    FMASK_SIGN        = 0b10000000000000000000000000000000,
    FMASK_EXPN        = 0b01111111100000000000000000000000,
    FMASK_FRAC        = 0b00000000011111111111111111111111,
    FMASK_QNAN        = 0b00000000010000000000000000000000,
    //                    ....xxxx....xxxx....xxxx....xxxx
    FFLAG_MASK        = 0b00000000000000000000000000011111,
    FFLAG_INVALID_OP  = 0b00000000000000000000000000010000,
    FFLAG_DIV_BY_ZERO = 0b00000000000000000000000000001000,
    FFLAG_OVERFLOW    = 0b00000000000000000000000000000100,
    FFLAG_UNDERFLOW   = 0b00000000000000000000000000000010,
    FFLAG_INEXACT     = 0b00000000000000000000000000000001,
    //                    ....xxxx....xxxx....xxxx....xxxx
    RV_NAN            = 0b01111111110000000000000000000000
};
/* clang-format on */

/* compute the fclass result */
static inline uint32_t calc_fclass(uint32_t f)
{
    const uint32_t sign = f & FMASK_SIGN;
    const uint32_t expn = f & FMASK_EXPN;
    const uint32_t frac = f & FMASK_FRAC;

    uint32_t out = 0;

    /*
     * 0x001    rs1 is -INF
     * 0x002    rs1 is negative normal
     * 0x004    rs1 is negative subnormal
     * 0x008    rs1 is -0
     * 0x010    rs1 is +0
     * 0x020    rs1 is positive subnormal
     * 0x040    rs1 is positive normal
     * 0x080    rs1 is +INF
     * 0x100    rs1 is a signaling NaN
     * 0x200    rs1 is a quiet NaN
     */

    /* Check the exponent bits */
    if (expn) {
        if (expn != FMASK_EXPN) {
            /* Check if it is negative normal or positive normal */
            out = sign ? 0x002 : 0x040;
        } else {
            /* Check if it is NaN */
            if (frac) {
                out = frac & FMASK_QNAN ? 0x200 : 0x100;
            } else if (!sign) {
                /* Check if it is +INF */
                out = 0x080;
            } else {
                /* Check if it is -INF */
                out = 0x001;
            }
        }
    } else if (frac) {
        /* Check if it is negative or positive subnormal */
        out = sign ? 0x004 : 0x020;
    } else {
        /* Check if it is +0 or -0 */
        out = sign ? 0x008 : 0x010;
    }

    return out;
}

static inline bool is_nan(uint32_t f)
{
    const uint32_t expn = f & FMASK_EXPN;
    const uint32_t frac = f & FMASK_FRAC;
    return (expn == FMASK_EXPN && frac);
}

static inline bool is_snan(uint32_t f)
{
    const uint32_t expn = f & FMASK_EXPN;
    const uint32_t frac = f & FMASK_FRAC;
    return (expn == FMASK_EXPN && frac && !(frac & FMASK_QNAN));
}
