/*
 * rv32emu is freely redistributable under the MIT License. See the file
 * "LICENSE" for information on usage and redistribution of this file.
 */

#if !RV32_HAS(SYSTEM)
#error "Do not manage to build this file unless you enable system support."
#endif

#include "riscv_private.h"

static bool ppn_is_valid(riscv_t *rv, uint32_t ppn)
{
    vm_attr_t *attr = PRIV(rv);
    const uint32_t nr_pg_max = attr->mem_size / RV_PG_SIZE;
    return ppn < nr_pg_max;
}

#define PAGE_TABLE(ppn)                                               \
    ppn_is_valid(rv, ppn)                                             \
        ? (uint32_t *) (attr->mem->mem_base + (ppn << (RV_PG_SHIFT))) \
        : NULL

/* Walk through page tables and get the corresponding PTE by virtual address if
 * exists
 * @rv: RISC-V emulator
 * @addr: virtual address
 * @level: the level of which the PTE is located
 * @return: NULL if a not found or fault else the corresponding PTE
 */
static uint32_t *mmu_walk(riscv_t *rv, const uint32_t addr, uint32_t *level)
{
    vm_attr_t *attr = PRIV(rv);
    uint32_t ppn = rv->csr_satp & MASK(22);

    /* root page table */
    uint32_t *page_table = PAGE_TABLE(ppn);
    if (!page_table)
        return NULL;

    for (int i = 1; i >= 0; i--) {
        *level = 2 - i;
        uint32_t vpn =
            (addr >> RV_PG_SHIFT >> (i * (RV_PG_SHIFT - 2))) & MASK(10);
        uint32_t *pte = page_table + vpn;

        uint8_t XWRV_bit = (*pte & MASK(4));
        switch (XWRV_bit) {
        case NEXT_PG_TBL: /* next level of the page table */
            ppn = (*pte >> (RV_PG_SHIFT - 2));
            page_table = PAGE_TABLE(ppn);
            if (!page_table)
                return NULL;
            break;
        case RO_PAGE:
        case RW_PAGE:
        case EO_PAGE:
        case RX_PAGE:
        case RWX_PAGE:
            ppn = (*pte >> (RV_PG_SHIFT - 2));
            if (*level == 1 &&
                unlikely(ppn & MASK(10))) /* misaligned superpage */
                return NULL;
            return pte; /* leaf PTE */
        case RESRV_PAGE1:
        case RESRV_PAGE2:
        default:
            return NULL;
        }
    }

    return NULL;
}

/* Verify the PTE and generate corresponding faults if needed
 * @op: the operation
 * @rv: RISC-V emulator
 * @pte: to be verified pte
 * @addr: the corresponding virtual address to cause fault
 * @return: false if a any fault is generated which caused by violating the
 * access permission else true
 */
/* FIXME: handle access fault, addr out of range check */
#define MMU_FAULT_CHECK(op, rv, pte, addr, access_bits) \
    mmu_##op##_fault_check(rv, pte, addr, access_bits)
#define MMU_FAULT_CHECK_IMPL(op, pgfault)                                     \
    static bool mmu_##op##_fault_check(riscv_t *rv, uint32_t *pte,            \
                                       uint32_t addr, uint32_t access_bits)   \
    {                                                                         \
        uint32_t scause;                                                      \
        uint32_t stval = addr;                                                \
        switch (access_bits) {                                                \
        case PTE_R:                                                           \
            scause = PAGEFAULT_LOAD;                                          \
            break;                                                            \
        case PTE_W:                                                           \
            scause = PAGEFAULT_STORE;                                         \
            break;                                                            \
        case PTE_X:                                                           \
            scause = PAGEFAULT_INSN;                                          \
            break;                                                            \
        default:                                                              \
            __UNREACHABLE;                                                    \
            break;                                                            \
        }                                                                     \
        if (pte && (!(*pte & PTE_V))) {                                       \
            SET_CAUSE_AND_TVAL_THEN_TRAP(rv, scause, stval);                  \
            return false;                                                     \
        }                                                                     \
        if (!(pte && (*pte & access_bits))) {                                 \
            SET_CAUSE_AND_TVAL_THEN_TRAP(rv, scause, stval);                  \
            return false;                                                     \
        }                                                                     \
        /*                                                                    \
         * (1) When MXR=0, only loads from pages marked readable (R=1) will   \
         * succeed.                                                           \
         *                                                                    \
         * (2) When MXR=1, loads from pages marked either readable or         \
         * executable (R=1 or X=1) will succeed.                              \
         */                                                                   \
        if (pte && ((!(SSTATUS_MXR & rv->csr_sstatus) && !(*pte & PTE_R) &&   \
                     (access_bits == PTE_R)) ||                               \
                    ((SSTATUS_MXR & rv->csr_sstatus) &&                       \
                     !((*pte & PTE_R) | (*pte & PTE_X)) &&                    \
                     (access_bits == PTE_R)))) {                              \
            SET_CAUSE_AND_TVAL_THEN_TRAP(rv, scause, stval);                  \
            return false;                                                     \
        }                                                                     \
        /*                                                                    \
         * When SUM=0, S-mode memory accesses to pages that are accessible by \
         * U-mode will fault.                                                 \
         */                                                                   \
        if (pte && rv->priv_mode == RV_PRIV_S_MODE &&                         \
            !(SSTATUS_SUM & rv->csr_sstatus) && (*pte & PTE_U)) {             \
            SET_CAUSE_AND_TVAL_THEN_TRAP(rv, scause, stval);                  \
            return false;                                                     \
        }                                                                     \
        /* PTE not found, map it in handler */                                \
        if (!pte) {                                                           \
            SET_CAUSE_AND_TVAL_THEN_TRAP(rv, scause, stval);                  \
            return false;                                                     \
        }                                                                     \
        /* valid PTE */                                                       \
        return true;                                                          \
    }

MMU_FAULT_CHECK_IMPL(ifetch, pagefault_insn)
MMU_FAULT_CHECK_IMPL(read, pagefault_load)
MMU_FAULT_CHECK_IMPL(write, pagefault_store)

#define get_ppn_and_offset()                                  \
    uint32_t ppn;                                             \
    uint32_t offset;                                          \
    do {                                                      \
        ppn = *pte >> (RV_PG_SHIFT - 2) << RV_PG_SHIFT;       \
        offset = level == 1 ? addr & MASK((RV_PG_SHIFT + 10)) \
                            : addr & MASK(RV_PG_SHIFT);       \
    } while (0)

/* The IO handler that operates when the Memory Management Unit (MMU)
 * is enabled during system emulation is responsible for managing
 * input/output operations. These callbacks are designed to implement
 * the riscv_io_t interface, ensuring compatibility and consistency to
 * the structure required by the interface. As a result, the riscv_io_t
 * interface can be reused.
 *
 * The IO handlers include:
 * - mmu_ifetch
 * - mmu_read_w
 * - mmu_read_s
 * - mmu_read_b
 * - mmu_write_w
 * - mmu_write_s
 * - mmu_write_b
 */
static uint32_t mmu_ifetch(riscv_t *rv, const uint32_t addr)
{
    if (!rv->csr_satp)
        return memory_ifetch(addr);

    uint32_t level;
    uint32_t *pte = mmu_walk(rv, addr, &level);
    bool ok = MMU_FAULT_CHECK(ifetch, rv, pte, addr, PTE_X);
    if (unlikely(!ok))
        pte = mmu_walk(rv, addr, &level);

    get_ppn_and_offset();
    return memory_ifetch(ppn | offset);
}

static uint32_t mmu_read_w(riscv_t *rv, const uint32_t addr)
{
    if (!rv->csr_satp)
        return memory_read_w(addr);

    uint32_t level;
    uint32_t *pte = mmu_walk(rv, addr, &level);
    bool ok = MMU_FAULT_CHECK(read, rv, pte, addr, PTE_R);
    if (unlikely(!ok))
        pte = mmu_walk(rv, addr, &level);

    get_ppn_and_offset();
    return memory_read_w(ppn | offset);
}

static uint16_t mmu_read_s(riscv_t *rv, const uint32_t addr)
{
    if (!rv->csr_satp)
        return memory_read_s(addr);

    uint32_t level;
    uint32_t *pte = mmu_walk(rv, addr, &level);
    bool ok = MMU_FAULT_CHECK(read, rv, pte, addr, PTE_R);
    if (unlikely(!ok))
        pte = mmu_walk(rv, addr, &level);

    get_ppn_and_offset();
    return memory_read_s(ppn | offset);
}

static uint8_t mmu_read_b(riscv_t *rv, const uint32_t addr)
{
    if (!rv->csr_satp)
        return memory_read_b(addr);

    uint32_t level;
    uint32_t *pte = mmu_walk(rv, addr, &level);
    bool ok = MMU_FAULT_CHECK(read, rv, pte, addr, PTE_R);
    if (unlikely(!ok))
        pte = mmu_walk(rv, addr, &level);

    get_ppn_and_offset();
    return memory_read_b(ppn | offset);
}

static void mmu_write_w(riscv_t *rv, const uint32_t addr, const uint32_t val)
{
    if (!rv->csr_satp)
        return memory_write_w(addr, (uint8_t *) &val);

    uint32_t level;
    uint32_t *pte = mmu_walk(rv, addr, &level);
    bool ok = MMU_FAULT_CHECK(write, rv, pte, addr, PTE_W);
    if (unlikely(!ok))
        pte = mmu_walk(rv, addr, &level);

    get_ppn_and_offset();
    memory_write_w(ppn | offset, (uint8_t *) &val);
}

static void mmu_write_s(riscv_t *rv, const uint32_t addr, const uint16_t val)
{
    if (!rv->csr_satp)
        return memory_write_s(addr, (uint8_t *) &val);

    uint32_t level;
    uint32_t *pte = mmu_walk(rv, addr, &level);
    bool ok = MMU_FAULT_CHECK(write, rv, pte, addr, PTE_W);
    if (unlikely(!ok))
        pte = mmu_walk(rv, addr, &level);

    get_ppn_and_offset();
    memory_write_s(ppn | offset, (uint8_t *) &val);
}

static void mmu_write_b(riscv_t *rv, const uint32_t addr, const uint8_t val)
{
    if (!rv->csr_satp)
        return memory_write_b(addr, (uint8_t *) &val);

    uint32_t level;
    uint32_t *pte = mmu_walk(rv, addr, &level);
    bool ok = MMU_FAULT_CHECK(write, rv, pte, addr, PTE_W);
    if (unlikely(!ok))
        pte = mmu_walk(rv, addr, &level);

    get_ppn_and_offset();
    memory_write_b(ppn | offset, (uint8_t *) &val);
}

riscv_io_t mmu_io = {
    /* memory read interface */
    .mem_ifetch = mmu_ifetch,
    .mem_read_w = mmu_read_w,
    .mem_read_s = mmu_read_s,
    .mem_read_b = mmu_read_b,

    /* memory write interface */
    .mem_write_w = mmu_write_w,
    .mem_write_s = mmu_write_s,
    .mem_write_b = mmu_write_b,

    /* system services or essential routines */
    .on_ecall = ecall_handler,
    .on_ebreak = ebreak_handler,
    .on_memcpy = memcpy_handler,
    .on_memset = memset_handler,
    .on_trap = trap_handler,
};
