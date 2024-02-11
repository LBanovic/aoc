#include "../utils.h"
#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define LIST_SIZE 512
#define max(a, b) ((a) >= (b) ? (a) : (b))
#define min(a, b) ((a) < (b) ? (a) : (b))

typedef long elemtype;

typedef struct {
  elemtype elements[LIST_SIZE];
  size_t size;
} List;

typedef struct {
  elemtype start;
  elemtype end;
  elemtype length;
} Interval;

typedef struct {
  Interval source;
  Interval destination;
} Range;

Range Range_parse(char *line) {
  Interval source = {-1, -1, -1};
  Interval destination = {-1, -1, -1};

  char *split = strtok(line, " ");
  while (split != NULL) {
    elemtype num = strtol(split, NULL, 10);
    if (destination.start == -1) {
      destination.start = num;
    } else if (source.start == -1) {
      source.start = num;
    } else {
      source.length = num;
      destination.length = num;

      source.end = source.start + source.length - 1;
      destination.end = destination.start + destination.length - 1;
    }
    split = strtok(NULL, " ");
  }
  Range range = {source, destination};
  return range;
}

#define NUM_RANGES 100
typedef struct {
  Range ranges[NUM_RANGES];
  size_t size;
} RangeBlock;

void List_add(List *list, elemtype val) {
  list->elements[list->size] = val;
  list->size++;
}

void parse_seeds(List *seeds, char *line) {
  char *split = strtok(line, " ");
  int part = 0;
  while (split != NULL) {
    if (part > 0) {
      List_add(seeds, strtol(split, NULL, 10));
    }
    part++;
    split = strtok(NULL, " ");
  }
}

void apply_ranges(List *seeds, RangeBlock *block) {
  for (int i = 0; i < seeds->size; i++) {
    for (int j = 0; j < block->size; j++) {
      elemtype element = seeds->elements[i];
      Interval source = block->ranges[j].source;
      Interval destination = block->ranges[j].destination;
      if (element >= source.start && element <= source.end) {
        seeds->elements[i] = element - source.start + destination.start;
        break;
      }
    }
  }
}

char input_buffer[LIST_SIZE] = {0};

void first_part(FILE *input) {
  List seeds = {0};
  RangeBlock block = {0};
  while (fgets(input_buffer, LIST_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    if (seeds.size == 0) {
      parse_seeds(&seeds, input_buffer);
    } else if (input_buffer[0] >= '0' && input_buffer[0] <= '9') {
      block.ranges[block.size] = Range_parse(input_buffer);
      block.size++;
    } else if (input_buffer[0] == 0) {
      apply_ranges(&seeds, &block);
      memset(&block, 0, sizeof(RangeBlock));
    }
  }
  apply_ranges(&seeds, &block);
  elemtype min = LONG_MAX;
  for (int i = 0; i < seeds.size; i++) {
    if (seeds.elements[i] < min) {
      min = seeds.elements[i];
    }
  }
  printf("%lu\n", min);
}

typedef struct {
  Interval seeds[LIST_SIZE];
  size_t size;
} SeedRange;

void SeedRange_parse(SeedRange *seed_range, char *line) {
  int counter = 0;
  char *split = strtok(line, " ");
  while (split != NULL) {
    if (counter > 0) {
      Interval *curr_interval = seed_range->seeds + seed_range->size;
      switch (counter % 2) {
      case 1:
        curr_interval->start = strtol(split, NULL, 10);
        break;
      case 0:
        curr_interval->length = strtol(split, NULL, 10);
        curr_interval->end = curr_interval->start + curr_interval->length - 1;
        seed_range->size++;
        break;
      }
    }
    split = strtok(NULL, " ");
    counter++;
  }
}

void SeedRange_add(SeedRange *seed_range, Interval interval) {
  seed_range->seeds[seed_range->size] = interval;
  seed_range->size++;
}

Interval SeedRange_pop(SeedRange *seed_range) {
  Interval interval = seed_range->seeds[0];
  memmove(seed_range->seeds, seed_range->seeds + 1,
          (seed_range->size - 1) * sizeof(Interval));
  seed_range->size--;
  return interval;
}

Interval Interval_intersection(Interval i1, Interval i2) {
  Interval inter = {0};
  inter.start = max(i1.start, i2.start);
  inter.end = min(i1.end, i2.end);
  inter.length = inter.end - inter.start + 1;
  return inter;
}

int Interval_is_in(Interval i1, Interval i2) {
  Interval intersection = Interval_intersection(i1, i2);
  return memcmp(&intersection, &i2, sizeof(i2));
}

int Interval_overlaps(Interval i1, Interval i2) {
  Interval intersection = Interval_intersection(i1, i2);
  return intersection.length > 0;
}

int Interval_difference(Interval i1, Interval i2, SeedRange *seeds) {
  Interval intersection = Interval_intersection(i1, i2);
  Interval left_part = {0};
  left_part.start = i1.start;
  left_part.end = intersection.start - 1;
  left_part.length = left_part.end - left_part.start + 1;
  if (left_part.length > 0) {
    SeedRange_add(seeds, left_part);
    return 1;
  }
  Interval right_part = {0};
  right_part.start = intersection.end + 1;
  right_part.end = i1.end;
  right_part.length = right_part.end - right_part.start + 1;
  if (right_part.length > 0) {
    SeedRange_add(seeds, right_part);
    return 1;
  }
  return 0;
}

SeedRange apply_intervals(SeedRange *seed_range, RangeBlock *block) {
  SeedRange next = {0};
  while (seed_range->size > 0) {
    Interval current = SeedRange_pop(seed_range);
    int added_something = 0;
    for (int j = 0; j < block->size; j++) {
      Interval source = block->ranges[j].source;
      Interval destination = block->ranges[j].destination;
      Interval intersection = Interval_intersection(current, source);
      if (intersection.length > 0) {
        Interval_difference(current, source, seed_range);
        intersection.start =
            intersection.start - source.start + destination.start;
        intersection.end = intersection.end - source.start + destination.start;
        SeedRange_add(&next, intersection);
        added_something = 1;
        break;
      }
    }
    if (!added_something) {
      SeedRange_add(&next, current);
    }
  }
  return next;
}

void second_part(FILE *input) {
  SeedRange seeds = {0};
  RangeBlock block = {0};
  while (fgets(input_buffer, LIST_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    if (seeds.size == 0) {
      SeedRange_parse(&seeds, input_buffer);
      for (int i = 0; i < seeds.size; i++) {
        Interval curr = seeds.seeds[i];
      }
    } else if (input_buffer[0] >= '0' && input_buffer[0] <= '9') {
      block.ranges[block.size] = Range_parse(input_buffer);
      block.size++;
    } else if (input_buffer[0] == 0) {
      if (block.size > 0) {
        seeds = apply_intervals(&seeds, &block);
        memset(&block, 0, sizeof(RangeBlock));
      }
    }
  }
  seeds = apply_intervals(&seeds, &block);
  elemtype min_seed = LONG_MAX;
  for (int i = 0; i < seeds.size; i++) {
    min_seed = min(min_seed, seeds.seeds[i].start);
  }
  printf("%ld\n", min_seed);
}

int main(int argc, char *argv[]) {
  process_input(argc, argv, first_part, second_part);
}
