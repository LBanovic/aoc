#include "../utils.h"
#include <stdio.h>
#include <string.h>

void first_part(FILE *input);
void second_part(FILE *input);

int main(int argc, char *argv[]) {

  return process_input(argc, argv, first_part, second_part);
}

#define ROCKMAP_SIZE 256

typedef struct {
  char lines[ROCKMAP_SIZE][ROCKMAP_SIZE];
  size_t line_count;
  size_t line_len;
} RockMap;

int RockMap_parse_from_file(FILE *input, RockMap *map) {
  while (1) {
    char *current_line = map->lines[map->line_count];
    char *retval = fgets(current_line, ROCKMAP_SIZE, input);
    if (retval == NULL) {
      return 0;
    }

    current_line[strcspn(current_line, "\n")] = 0;
    size_t line_len = strnlen(current_line, ROCKMAP_SIZE);
    if (line_len == 0) {
      return 1;
    }
    if (map->line_len == 0) {
      map->line_len = line_len;
    }
    map->line_count++;
  }
}

int check_surrounding(RockMap *map, int i) {
  for (int j = 1; i - j >= 0 && i + j + 1 < map->line_count; j++) {
    if (memcmp(map->lines[i - j], map->lines[i + j + 1], map->line_len) != 0) {
      return 0;
    }
  }
  return 1;
}

int check(RockMap *map) {
  for (int i = 0; i < map->line_count - 1; i++) {
    if (memcmp(map->lines[i], map->lines[i + 1], map->line_len) == 0 &&
        check_surrounding(map, i)) {
      return i + 1;
    }
  }
  return 0;
}

void RockMap_transpose(RockMap *map) {
  RockMap other = {0};
  for (int i = 0; i < map->line_count; i++) {
    for (int j = 0; j < map->line_len; j++) {
      other.lines[j][i] = map->lines[i][j];
    }
  }
  other.line_len = map->line_count;
  other.line_count = map->line_len;
  *map = other;
}

void first_part(FILE *input) {
  int has_next;
  int sum = 0;
  do {
    RockMap map = {0};
    has_next = RockMap_parse_from_file(input, &map);
    sum += 100 * check(&map);
    RockMap_transpose(&map);
    sum += check(&map);
  } while (has_next);
  printf("%d\n", sum);
}

int check_not_invalid(RockMap *map, int invalid_val) {
  for (int i = 0; i < map->line_count - 1; i++) {
    if (i + 1 == invalid_val) {
      continue;
    }
    if (memcmp(map->lines[i], map->lines[i + 1], map->line_len) == 0 &&
        check_surrounding(map, i)) {
      return i + 1;
    }
  }
  return 0;
}
int check_modified(RockMap map, int i, int j, int invalid_val) {
  if (i >= 0 && j >= 0) {
    map.lines[i][j] = (map.lines[i][j] == '#' ? '.' : '#');
  }
  int row_check = check_not_invalid(&map, invalid_val);
  return row_check;
}

int check_all_combinations(RockMap *map) {
  int unmodified_value = check(map);
  for (int i = 0; i < map->line_count; i++) {
    for (int j = 0; j < map->line_len; j++) {
      int modified_value = check_modified(*map, i, j, unmodified_value);
      if (modified_value != 0) {
        return modified_value;
      }
    }
  }
  return 0;
}

void second_part(FILE *input) {
  int has_next;
  int sum = 0;
  do {
    RockMap map = {0};
    has_next = RockMap_parse_from_file(input, &map);
    sum += 100 * check_all_combinations(&map);
    RockMap_transpose(&map);
    sum += check_all_combinations(&map);
  } while (has_next);
  printf("%d\n", sum);
}
