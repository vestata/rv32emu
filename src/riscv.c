/*
 * rv32emu is freely redistributable under the MIT License. See the file
 * "LICENSE" for information on usage and redistribution of this file.
 */

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "mpool.h"
#include "riscv.h"
#include "riscv_private.h"
#include "utils.h"
#if RV32_HAS(JIT)
#include "cache.h"
#include "jit.h"
#define CODE_CACHE_SIZE (1024 * 1024)
#endif

#define BLOCK_IR_MAP_CAPACITY_BITS 10

#if !RV32_HAS(JIT)
/* initialize the block map */
static void block_map_init(block_map_t *map, const uint8_t bits)
{
    map->block_capacity = 1 << bits;
    map->size = 0;
    map->map = calloc(map->block_capacity, sizeof(struct block *));
    assert(map->map);
}

/* clear all block in the block map */
void block_map_clear(riscv_t *rv)
{
    block_map_t *map = &rv->block_map;
    for (uint32_t i = 0; i < map->block_capacity; i++) {
        block_t *block = map->map[i];
        if (!block)
            continue;
        uint32_t idx;
        rv_insn_t *ir, *next;
        for (idx = 0, ir = block->ir_head; idx < block->n_insn;
             idx++, ir = next) {
            free(ir->fuse);
            free(ir->branch_table);
            next = ir->next;
            mpool_free(rv->block_ir_mp, ir);
        }
        mpool_free(rv->block_mp, block);
        map->map[i] = NULL;
    }
    map->size = 0;
}

static void block_map_destroy(riscv_t *rv)
{
    block_map_clear(rv);
    free(rv->block_map.map);

    mpool_destroy(rv->block_mp);
    mpool_destroy(rv->block_ir_mp);
}
#endif

riscv_user_t rv_userdata(riscv_t *rv)
{
    assert(rv);
    return rv->userdata;
}

bool rv_set_pc(riscv_t *rv, riscv_word_t pc)
{
    assert(rv);
#if RV32_HAS(EXT_C)
    if (pc & 1)
#else
    if (pc & 3)
#endif
        return false;

    rv->PC = pc;
    return true;
}

riscv_word_t rv_get_pc(riscv_t *rv)
{
    assert(rv);
    return rv->PC;
}

void rv_set_reg(riscv_t *rv, uint32_t reg, riscv_word_t in)
{
    assert(rv);
    if (reg < N_RV_REGS && reg != rv_reg_zero)
        rv->X[reg] = in;
}

riscv_word_t rv_get_reg(riscv_t *rv, uint32_t reg)
{
    assert(rv);
    if (reg < N_RV_REGS)
        return rv->X[reg];

    return ~0U;
}

riscv_t *rv_create(const riscv_io_t *io,
                   riscv_user_t userdata,
                   int argc,
                   char **args,
                   bool output_exit_code)
{
    assert(io);

    riscv_t *rv = calloc(1, sizeof(riscv_t));
    assert(rv);

    /* copy over the IO interface */
    memcpy(&rv->io, io, sizeof(riscv_io_t));

    /* copy over the userdata */
    rv->userdata = userdata;

    rv->output_exit_code = output_exit_code;

    /* create block and IRs memory pool */
    rv->block_mp = mpool_create(sizeof(block_t) << BLOCK_MAP_CAPACITY_BITS,
                                sizeof(block_t));
    rv->block_ir_mp = mpool_create(
        sizeof(rv_insn_t) << BLOCK_IR_MAP_CAPACITY_BITS, sizeof(rv_insn_t));

#if !RV32_HAS(JIT)
    /* initialize the block map */
    block_map_init(&rv->block_map, BLOCK_MAP_CAPACITY_BITS);
#else
    rv->chain_entry_mp =
        mpool_create(sizeof(chain_entry_t) << BLOCK_IR_MAP_CAPACITY_BITS,
                     sizeof(chain_entry_t));
    rv->jit_state = jit_state_init(CODE_CACHE_SIZE);
    rv->block_cache = cache_create(BLOCK_MAP_CAPACITY_BITS);
    assert(rv->block_cache);
#endif
    /* reset */
    rv_reset(rv, 0U, argc, args);

    return rv;
}

void rv_halt(riscv_t *rv)
{
    rv->halt = true;
}

bool rv_has_halted(riscv_t *rv)
{
    return rv->halt;
}

bool rv_enables_to_output_exit_code(riscv_t *rv)
{
    return rv->output_exit_code;
}

void rv_delete(riscv_t *rv)
{
    assert(rv);
#if !RV32_HAS(JIT)
    block_map_destroy(rv);
#else
    mpool_destroy(rv->chain_entry_mp);
    jit_state_exit(rv->jit_state);
    cache_free(rv->block_cache);
#endif
    free(rv);
}

void rv_reset(riscv_t *rv, riscv_word_t pc, int argc, char **args)
{
    assert(rv);
    memset(rv->X, 0, sizeof(uint32_t) * N_RV_REGS);

    /* set the reset address */
    rv->PC = pc;

    /* set the default stack pointer */
    rv->X[rv_reg_sp] = DEFAULT_STACK_ADDR;

    /* Store 'argc' and 'args' of the target program in 'state->mem'. Thus,
     * we can use an offset trick to emulate 32/64-bit target programs on
     * a 64-bit built emulator.
     *
     * memory layout of arguments as below:
     * -----------------------
     * |    NULL            |
     * -----------------------
     * |    envp[n]         |
     * -----------------------
     * |    envp[n - 1]     |
     * -----------------------
     * |    ...             |
     * -----------------------
     * |    envp[0]         |
     * -----------------------
     * |    NULL            |
     * -----------------------
     * |    args[n]         |
     * -----------------------
     * |    args[n - 1]     |
     * -----------------------
     * |    ...             |
     * -----------------------
     * |    args[0]         |
     * -----------------------
     * |    argc            |
     * -----------------------
     *
     * TODO: access to envp
     */

    state_t *s = rv_userdata(rv);

    /* copy args to RAM */
    uintptr_t args_size = (1 + argc + 1) * sizeof(uint32_t);
    uintptr_t args_bottom = DEFAULT_ARGS_ADDR;
    uintptr_t args_top = args_bottom - args_size;
    args_top &= 16;

    /* argc */
    uintptr_t *args_p = (uintptr_t *) args_top;
    memory_write(s->mem, (uintptr_t) args_p, (void *) &argc, sizeof(int));
    args_p++;

    /* args */
    /* used for calculating the offset of args when pushing to stack */
    size_t args_space[256];
    size_t args_space_idx = 0;
    size_t args_len;
    size_t args_len_total = 0;
    for (int i = 0; i < argc; i++) {
        const char *arg = args[i];
        args_len = strlen(arg);
        memory_write(s->mem, (uintptr_t) args_p, (void *) arg,
                     (args_len + 1) * sizeof(uint8_t));
        args_space[args_space_idx++] = args_len + 1;
        args_p = (uintptr_t *) ((uintptr_t) args_p + args_len + 1);
        args_len_total += args_len + 1;
    }
    args_p = (uintptr_t *) ((uintptr_t) args_p - args_len_total);
    args_p--; /* point to argc */

    /* ready to push argc, args to stack */
    int stack_size = (1 + argc + 1) * sizeof(uint32_t);
    uintptr_t stack_bottom = (uintptr_t) rv->X[rv_reg_sp];
    uintptr_t stack_top = stack_bottom - stack_size;
    stack_top &= -16;

    /* argc */
    uintptr_t *sp = (uintptr_t *) stack_top;
    memory_write(s->mem, (uintptr_t) sp,
                 (void *) (s->mem->mem_base + (uintptr_t) args_p), sizeof(int));
    args_p++;
    /* keep argc and args[0] within one word due to RV32 ABI */
    sp = (uintptr_t *) ((uint32_t *) sp + 1);

    /* args */
    for (int i = 0; i < argc; i++) {
        uintptr_t offset = (uintptr_t) args_p;
        memory_write(s->mem, (uintptr_t) sp, (void *) &offset,
                     sizeof(uintptr_t));
        args_p = (uintptr_t *) ((uintptr_t) args_p + args_space[i]);
        sp = (uintptr_t *) ((uint32_t *) sp + 1);
    }
    memory_fill(s->mem, (uintptr_t) sp, sizeof(uint32_t), 0);

    /* reset sp pointing to argc */
    rv->X[rv_reg_sp] = stack_top;

    /* reset the csrs */
    rv->csr_mtvec = 0;
    rv->csr_cycle = 0;
    rv->csr_mstatus = 0;
    rv->csr_misa |= MISA_SUPER | MISA_USER | MISA_I;
#if RV32_HAS(EXT_A)
    rv->csr_misa |= MISA_A;
#endif
#if RV32_HAS(EXT_C)
    rv->csr_misa |= MISA_C;
#endif
#if RV32_HAS(EXT_M)
    rv->csr_misa |= MISA_M;
#endif
#if RV32_HAS(EXT_F)
    rv->csr_misa |= MISA_F;
    /* reset float registers */
    for (int i = 0; i < N_RV_REGS; i++)
        rv->F[i].v = 0;
    rv->csr_fcsr = 0;
#endif

    rv->halt = false;
}

state_t *state_new(void)
{
    state_t *s = malloc(sizeof(state_t));
    assert(s);
    s->mem = memory_new();
    s->break_addr = 0;

    s->fd_map = map_init(int, FILE *, map_cmp_int);
    FILE *files[] = {stdin, stdout, stderr};
    for (size_t i = 0; i < ARRAYS_SIZE(files); i++)
        map_insert(s->fd_map, &i, &files[i]);

    return s;
}

void state_delete(state_t *s)
{
    if (!s)
        return;

    map_delete(s->fd_map);
    memory_delete(s->mem);
    free(s);
}

static const char *insn_name_table[] = {
#define _(inst, can_branch, insn_len, translatable, reg_mask) \
    [rv_insn_##inst] = #inst,
    RV_INSN_LIST
#undef _
#define _(inst) [rv_insn_##inst] = #inst,
        FUSE_INSN_LIST
#undef _
};

#if RV32_HAS(JIT)
void profile(block_t *block, uint32_t freq, FILE *output_file)
{
    fprintf(output_file, "%#-9x|", block->pc_start);
    fprintf(output_file, "%#-8x|", block->pc_end);
    fprintf(output_file, " %-10u|", freq);
    fprintf(output_file, " %-5s |", block->hot ? "true" : "false");
    fprintf(output_file, " %-8s |", block->backward ? "true" : "false");
    fprintf(output_file, " %-6s |", block->has_loops ? "true" : "false");
    rv_insn_t *taken = block->ir_tail->branch_taken,
              *untaken = block->ir_tail->branch_untaken;
    if (untaken)
        fprintf(output_file, "%#-9x|", untaken->pc);
    else
        fprintf(output_file, "%-9s|", "NULL");
    if (taken)
        fprintf(output_file, "%#-8x|", taken->pc);
    else
        fprintf(output_file, "%-8s|", "NULL");
    rv_insn_t *ir = block->ir_head;
    while (1) {
        assert(ir);
        fprintf(output_file, "%s", insn_name_table[ir->opcode]);
        if (!ir->next)
            break;
        ir = ir->next;
        fprintf(output_file, " - ");
    }
    fprintf(output_file, "\n");
}
#endif

void rv_profile(riscv_t *rv, char *out_file_path)
{
    if (!out_file_path) {
        fprintf(stderr, "Profiling data output file is NULL.\n");
        return;
    }
    FILE *f = fopen(out_file_path, "w");
    if (!f) {
        fprintf(stderr, "Cannot open profiling data output file.\n");
        return;
    }
#if RV32_HAS(JIT)
    fprintf(f,
            "PC start |PC end  | frequency |  hot  | backward |  loop  | "
            "untaken | taken  "
            "| IR "
            "list \n");
    cache_profile(rv->block_cache, f, (prof_func_t) profile);
#else
    fprintf(f, "PC start |PC end  | untaken | taken  | IR list \n");
    block_map_t *map = &rv->block_map;
    for (uint32_t i = 0; i < map->block_capacity; i++) {
        block_t *block = map->map[i];
        if (!block)
            continue;
        fprintf(f, "%#-9x|", block->pc_start);
        fprintf(f, "%#-8x|", block->pc_end);
        rv_insn_t *taken = block->ir_tail->branch_taken,
                  *untaken = block->ir_tail->branch_untaken;
        if (untaken)
            fprintf(f, "%#-9x|", untaken->pc);
        else
            fprintf(f, "%-9s|", "NULL");
        if (taken)
            fprintf(f, "%#-8x|", taken->pc);
        else
            fprintf(f, "%-8s|", "NULL");
        rv_insn_t *ir = block->ir_head;
        while (1) {
            assert(ir);
            fprintf(f, "%s", insn_name_table[ir->opcode]);
            if (!ir->next)
                break;
            ir = ir->next;
            fprintf(f, " - ");
        }
        fprintf(f, "\n");
    }
#endif
}
