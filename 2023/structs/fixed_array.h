#ifndef FIXED_ARRAY_H
#define FIXED_ARRAY_H
#include <assert.h>
#include <stddef.h>

#define fixed_array_append(fixed_array, item)                                  \
  do {                                                                         \
    size_t arrlen =                                                            \
        sizeof((fixed_array)->items) / sizeof((fixed_array)->items[0]);        \
    assert((fixed_array)->size < arrlen);                                      \
    (fixed_array)->items[(fixed_array)->size] = item;                          \
    (fixed_array)->size++;                                                     \
  } while (0);

#define fixed_array_pop(fixed_array, position, output)                         \
  do {                                                                         \
    assert(fixed_array->size > 0 && position < fixed_array->size);             \
    if (output) {                                                              \
      (*(output)) = fixed_array->items[position];                              \
    }                                                                          \
    memmove(fixed_array->items + position, fixed_array->items + position + 1,  \
            (fixed_array->size - (position + 1)) *                             \
                sizeof(fixed_array->items[0]));                                \
    fixed_array->size--;                                                       \
  } while (0);

/**
 * Check if a given `item` is in the provided `fixed_array`.  `out_param` is set
 * to 0 if it is not present, otherwise it is set to 1.
 * The comparison function takes pointers to items to compare and returns 0 if
 * the elements are the same, and non-0 if they are different.
 *
 * Input parameters:
 *  fixed_array - A pointer to a fixed array
 *  item - a pointer to an item to look for
 *  eq_op - comparison function
 *
 * Output parameters:
 *  out_param - pointer to an integer variable where the result will be stored.
 */
#define fixed_array_index_of(fixed_array, item, eq_op, out_param)              \
  do {                                                                         \
    (*(out_param)) = -1;                                                       \
    for (int i = 0; i < fixed_array->size; i++) {                              \
      if (eq_op(&fixed_array->items[i], item)) {                               \
        (*(out_param)) = i;                                                    \
        break;                                                                 \
      }                                                                        \
    }                                                                          \
  } while (0);

#endif /* ifndef FIXED_ARRAY_H*/
