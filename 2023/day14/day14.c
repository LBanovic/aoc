#include "../utils.h"
#include <string.h>

void first_part(FILE *input);
void second_part(FILE *input);

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}

#define MAX_ROWSIZE 140
#define MAX_COLSIZE 140

typedef struct {
  char positions[MAX_ROWSIZE][MAX_COLSIZE];
  size_t line_count;
  size_t line_len;
} Map;

Map Map_tilt(Map *map, int *sum) {
  Map tilted = *map;
  int curr_row;
  *sum = 0;
  for (int i = 0; i < map->line_count; i++) {
    for (int j = 0; j < map->line_len; j++) {
      if (map->positions[i][j] == 'O') {
        curr_row = i;
        while (curr_row > 0 && tilted.positions[curr_row - 1][j] == '.') {
          tilted.positions[curr_row][j] = '.';
          tilted.positions[curr_row - 1][j] = 'O';
          curr_row--;
        }
        *sum += map->line_count - curr_row;
      }
    }
  }
  return tilted;
}

void first_part(FILE *input) {
  Map map = {0};
  do {
    char *curr_row = fgets(map.positions[map.line_count], MAX_COLSIZE, input);
    if (!curr_row) {
      break;
    }
    curr_row[strcspn(curr_row, "\n")] = 0;
    map.line_count++;
    map.line_len = strnlen(curr_row, MAX_ROWSIZE);
  } while (1);

  int sum;
  map = Map_tilt(&map, &sum);
  printf("%d\n", sum);
}

char Map_get_at_pos(Map *map, int i, int j) {
  if (i < 0 || i >= map->line_count || j < 0 || j >= map->line_len) {
    return '#';
  }
  return map->positions[i][j];
}

Map Map_cycle(Map *map) {
  Map tilted = *map;
  int curr_row;
  int curr_col;

  // NORTH
  for (int i = 0; i < map->line_count; i++) {
    for (int j = 0; j < map->line_len; j++) {
      if (map->positions[i][j] == 'O') {
        curr_row = i;
        while (curr_row > 0 && tilted.positions[curr_row - 1][j] == '.') {
          tilted.positions[curr_row][j] = '.';
          tilted.positions[curr_row - 1][j] = 'O';
          curr_row--;
        }
      }
    }
  }
  *map = tilted;

  // WEST
  for (int i = 0; i < map->line_count; i++) {
    for (int j = 0; j < map->line_len; j++) {
      if (map->positions[i][j] == 'O') {
        curr_col = j;
        while (curr_col > 0 && tilted.positions[i][curr_col - 1] == '.') {
          tilted.positions[i][curr_col] = '.';
          tilted.positions[i][curr_col - 1] = 'O';
          curr_col--;
        }
      }
    }
  }

  *map = tilted;
  // SOUTH
  for (int i = map->line_count - 1; i >= 0; i--) {
    for (int j = 0; j < map->line_len; j++) {
      if (map->positions[i][j] == 'O') {
        curr_row = i;
        while (curr_row < map->line_count - 1 &&
               tilted.positions[curr_row + 1][j] == '.') {
          tilted.positions[curr_row][j] = '.';
          tilted.positions[curr_row + 1][j] = 'O';
          curr_row++;
        }
      }
    }
  }
  *map = tilted;
  // EAST
  for (int i = 0; i < map->line_count; i++) {
    for (int j = map->line_len - 1; j >= 0; j--) {
      if (map->positions[i][j] == 'O') {
        curr_col = j;
        while (curr_col < map->line_count - 1 &&
               tilted.positions[i][curr_col + 1] == '.') {
          tilted.positions[i][curr_col] = '.';
          tilted.positions[i][curr_col + 1] = 'O';
          curr_col++;
        }
      }
    }
  }
  return tilted;
}

int Map_get_sum(Map *map) {
  int sum = 0;
  for (int i = 0; i < map->line_count; i++) {
    for (int j = 0; j < map->line_len; j++) {
      if (map->positions[i][j] == 'O') {
        sum += map->line_count - i;
      }
    }
  }
  return sum;
}

#define MAP_CACHE_SIZE 256

typedef struct {
  Map maps[MAP_CACHE_SIZE];
  size_t size;
} MapCache;

void MapCache_add(MapCache *cache, Map *map) {
  cache->maps[cache->size] = *map;
  cache->size++;
}

int MapCache_index(MapCache *cache, Map *map) {
  for (int i = 0; i < cache->size; i++) {
    if (memcmp(cache->maps + i, map, sizeof(Map)) == 0) {
      return i;
    }
  }
  return -1;
}

void second_part(FILE *input) {
  Map map = {0};
  MapCache cache = {0};
  do {
    char *curr_row = fgets(map.positions[map.line_count], MAX_COLSIZE, input);
    if (!curr_row) {
      break;
    }
    curr_row[strcspn(curr_row, "\n")] = 0;
    map.line_count++;
    map.line_len = strnlen(curr_row, MAX_ROWSIZE);
  } while (1);

  int index_of_repeat = 0;
  do {
    index_of_repeat = MapCache_index(&cache, &map);
    if (index_of_repeat >= 0) {
      break;
    }
    MapCache_add(&cache, &map);
    map = Map_cycle(&map);
  } while (1);
  long n_repeats = 1000000000;
  int index_of_final =
      (n_repeats - index_of_repeat) % (cache.size - index_of_repeat) +
      index_of_repeat;
  printf("%d\n", Map_get_sum(cache.maps + index_of_final));
}
