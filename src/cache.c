/*
 * rv32emu is freely redistributable under the MIT License. See the file
 * "LICENSE" for information on usage and redistribution of this file.
 */

#include <assert.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "cache.h"
#include "mpool.h"
#include "utils.h"

static uint32_t cache_size, cache_size_bits;

/* hash function for the cache */
HASH_FUNC_IMPL(cache_hash, cache_size_bits, cache_size)

struct hlist_head {
    struct hlist_node *first;
};

struct hlist_node {
    struct hlist_node *next, **pprev;
};

typedef struct {
    void *value;
    bool alive; /* indicates whether this cache is alive or a history of evicted
                   cache in hash map */
    uint32_t key;
    uint32_t freq;
    struct list_head list;
    struct hlist_node ht_list;
} cache_entry_t;

typedef struct {
    struct hlist_head *ht_list_head;
} hashtable_t;

/*
 * The cache utilizes the degenerated adaptive replacement cache (ARC), which
 * has only least-recently-used (LRU) and ignores least-frequently-used (LFU)
 * part. The frequently used cache will be compiled to the binary of target
 * platform by the just-in-time (JIT) compiler, so that it doesn't need to be
 * preserved in cache anymore. When the cache is full, the least used cache is
 * going to be evicted to the ghost list as the history. If the key of the
 * inserted entry matches the one in the ghost list, the history will be
 * detached and freed, and the stored information will be inherited by the new
 * entry.
 */
typedef struct cache {
    struct list_head list;       /* list of live cache */
    struct list_head ghost_list; /* list of evicted cache */
    hashtable_t map; /* hash map which contains both live and evicted cache */
    uint32_t size;
    uint32_t ghost_list_size;
    uint32_t capacity;
} cache_t;

#define INIT_HLIST_HEAD(ptr) ((ptr)->first = NULL)

static inline void INIT_HLIST_NODE(struct hlist_node *h)
{
    h->next = NULL;
    h->pprev = NULL;
}

static inline int hlist_empty(const struct hlist_head *h)
{
    return !h->first;
}

static inline void hlist_add_head(struct hlist_node *n, struct hlist_head *h)
{
    struct hlist_node *first = h->first;
    n->next = first;
    if (first)
        first->pprev = &n->next;

    h->first = n;
    n->pprev = &h->first;
}

static inline bool hlist_unhashed(const struct hlist_node *h)
{
    return !h->pprev;
}

static inline void hlist_del(struct hlist_node *n)
{
    struct hlist_node *next = n->next;
    struct hlist_node **pprev = n->pprev;

    *pprev = next;
    if (next)
        next->pprev = pprev;
}

static inline void hlist_del_init(struct hlist_node *n)
{
    if (hlist_unhashed(n))
        return;
    hlist_del(n);
    INIT_HLIST_NODE(n);
}

#define hlist_entry(ptr, type, member) container_of(ptr, type, member)

#ifdef __HAVE_TYPEOF
#define hlist_entry_safe(ptr, type, member)                  \
    ({                                                       \
        typeof(ptr) ____ptr = (ptr);                         \
        ____ptr ? hlist_entry(____ptr, type, member) : NULL; \
    })
#else
#define hlist_entry_safe(ptr, type, member) \
    (ptr) ? hlist_entry(ptr, type, member) : NULL
#endif

/* clang-format off */
#ifdef __HAVE_TYPEOF
#define hlist_for_each_entry(pos, head, member)                              \
    for (pos = hlist_entry_safe((head)->first, typeof(*(pos)), member); pos; \
         pos = hlist_entry_safe((pos)->member.next, typeof(*(pos)), member))

#define hlist_for_each_entry_safe(pos, n, head, member)               \
    for (pos = hlist_entry_safe((head)->first, typeof(*pos), member); \
         pos && ({ n = pos->member.next; 1; });                       \
         pos = hlist_entry_safe(n, typeof(*pos), member))
#else
#define hlist_for_each_entry(pos, head, member, type)              \
    for (pos = hlist_entry_safe((head)->first, type, member); pos; \
         pos = hlist_entry_safe((pos)->member.next, type, member))

#define hlist_for_each_entry_safe(pos, n, head, member, type) \
    for (pos = hlist_entry_safe((head)->first, type, member); \
         pos && ({ n = pos->member.next; 1; });               \
         pos = hlist_entry_safe(n, type, member))
#endif
/* clang-format on */

cache_t *cache_create(uint32_t size_bits)
{
    cache_t *cache = malloc(sizeof(cache_t));
    if (!cache)
        return NULL;

    cache_size_bits = size_bits;
    cache_size = 1 << size_bits;

    INIT_LIST_HEAD(&cache->list);
    INIT_LIST_HEAD(&cache->ghost_list);
    cache->size = 0;
    cache->ghost_list_size = 0;
    cache->capacity = cache_size;

    cache->map.ht_list_head = malloc(cache_size * sizeof(struct hlist_head));
    if (!cache->map.ht_list_head) {
        free(cache);
        return NULL;
    }

    for (uint32_t i = 0; i < cache_size; i++)
        INIT_HLIST_HEAD(&cache->map.ht_list_head[i]);

    return cache;
}

void *cache_get(const cache_t *cache, uint32_t key, bool update)
{
    if (unlikely(!cache->capacity))
        return NULL;

    if (hlist_empty(&cache->map.ht_list_head[cache_hash(key)]))
        return NULL;

    cache_entry_t *entry = NULL;
#ifdef __HAVE_TYPEOF
    hlist_for_each_entry (entry, &cache->map.ht_list_head[cache_hash(key)],
                          ht_list)
#else
    hlist_for_each_entry (entry, &cache->map.ht_list_head[cache_hash(key)],
                          ht_list, cache_entry_t)
#endif
    {
        if (entry->key == key)
            break;
    }

    /* return NULL if cache miss */
    if (!entry || entry->key != key || !entry->alive)
        return NULL;

    /*
     * FIXME: In system simulation, there might be several identical PC from
     * different processes. We need to check the SATP CSR to update the correct
     * entry.
     */
    /* When the frequency of use for a specific block exceeds the predetermined
     * THRESHOLD, the block is dispatched to the code generator to generate C
     * code. The generated C code is then compiled into machine code by the
     * target compiler.
     */
    if (update)
        entry->freq++;

    return entry->value;
}

/*
 * When the size of ghost list reaches the limit, the oldest history is going to
 * be dropped. The stored information will be lost forever.
 */
FORCE_INLINE void cache_ghost_list_update(cache_t *cache)
{
    if (cache->ghost_list_size <= cache->capacity)
        return;

    cache_entry_t *entry =
        list_last_entry(&cache->ghost_list, cache_entry_t, list);
    assert(!entry->alive);
    hlist_del_init(&entry->ht_list);
    list_del_init(&entry->list);
    cache->ghost_list_size--;
    free(entry);
}

/*
 * For a cache insertion, it might be the one which:
 * - evicts the least recently used cache
 * - updates the existing cache
 * - retrieves the information from the history in the glost list
 */
void *cache_put(cache_t *cache, uint32_t key, void *value)
{
    assert(cache->size <= cache->capacity);

    cache_entry_t *replaced = NULL, *revived = NULL, *entry;
#ifdef __HAVE_TYPEOF
    hlist_for_each_entry (entry, &cache->map.ht_list_head[cache_hash(key)],
                          ht_list)
#else
    hlist_for_each_entry (entry, &cache->map.ht_list_head[cache_hash(key)],
                          ht_list, cache_entry_t)
#endif
    {
        if (entry->key != key)
            continue;
        if (!entry->alive) {
            revived = entry;
            break;
        }
        /* update the existing cache */
        if (entry->value != value) {
            replaced = entry;
            break;
        }
        /* should not put an identical block to cache */
        assert(NULL);
        __UNREACHABLE;
    }

    /* get the entry to be replaced if cache is full */
    if (!replaced && cache->size == cache->capacity) {
        replaced = list_last_entry(&cache->list, cache_entry_t, list);
        assert(replaced);
    }

    void *replaced_value = NULL;
    if (replaced) {
        assert(replaced->alive);

        replaced_value = replaced->value;
        replaced->alive = false;
        list_del_init(&replaced->list);
        cache->size--;
        list_add(&replaced->list, &cache->ghost_list);
        cache->ghost_list_size++;
    }

    cache_entry_t *new_entry = calloc(1, sizeof(cache_entry_t));
    assert(new_entry);

    INIT_LIST_HEAD(&new_entry->list);
    INIT_HLIST_NODE(&new_entry->ht_list);
    new_entry->key = key;
    new_entry->value = value;
    new_entry->alive = true;

    if (!revived) {
        new_entry->freq = 1;
    } else {
        new_entry->freq = revived->freq + 1;
        hlist_del_init(&revived->ht_list);
        list_del_init(&revived->list);
        cache->ghost_list_size--;
        free(revived);
    }

    list_add(&new_entry->list, &cache->list);
    hlist_add_head(&new_entry->ht_list,
                   &cache->map.ht_list_head[cache_hash(key)]);

    cache->size++;

    cache_ghost_list_update(cache);

    assert(cache->size <= cache->capacity);
    assert(cache->ghost_list_size <= cache->capacity);
    return replaced_value;
}

void cache_free(cache_t *cache)
{
    free(cache->map.ht_list_head);
    free(cache);
}

uint32_t cache_freq(const struct cache *cache, uint32_t key)
{
    if (unlikely(!cache->capacity))
        return 0;

    if (hlist_empty(&cache->map.ht_list_head[cache_hash(key)]))
        return 0;

    cache_entry_t *entry = NULL;
#ifdef __HAVE_TYPEOF
    hlist_for_each_entry (entry, &cache->map.ht_list_head[cache_hash(key)],
                          ht_list)
#else
    hlist_for_each_entry (entry, &cache->map.ht_list_head[cache_hash(key)],
                          ht_list, cache_entry_t)
#endif
    {
        if (entry->key == key && entry->alive)
            return entry->freq;
    }
    return 0;
}

#if RV32_HAS(JIT)
bool cache_hot(const struct cache *cache, uint32_t key)
{
    if (unlikely(!cache->capacity))
        return false;

    if (hlist_empty(&cache->map.ht_list_head[cache_hash(key)]))
        return false;

    cache_entry_t *entry = NULL;
#ifdef __HAVE_TYPEOF
    hlist_for_each_entry (entry, &cache->map.ht_list_head[cache_hash(key)],
                          ht_list)
#else
    hlist_for_each_entry (entry, &cache->map.ht_list_head[cache_hash(key)],
                          ht_list, cache_entry_t)
#endif
    {
        if (entry->key == key && entry->alive && entry->freq >= THRESHOLD) {
            return true;
        }
    }
    return false;
}
void cache_profile(const struct cache *cache,
                   FILE *output_file,
                   prof_func_t func)
{
    assert(cache);
    assert(func);
    assert(output_file);

    cache_entry_t *entry;
#ifdef __HAVE_TYPEOF
    list_for_each_entry (entry, &cache->list, list)
#else
    list_for_each_entry (entry, &cache->list, list, cache_entry_t)
#endif
    {
        func(entry->value, entry->freq, output_file);
    }
}

void clear_cache_hot(const struct cache *cache, clear_func_t func)
{
    assert(cache);
    assert(func);

    cache_entry_t *entry = NULL;
#ifdef __HAVE_TYPEOF
    list_for_each_entry (entry, &cache->list, list)
#else
    list_for_each_entry (entry, &cache->list, list, cache_entry_t)
#endif
    {
        func(entry->value);
    }
}
#endif
