#include "../utils.h"
#include <locale.h>
#include <stdio.h>
#include <string.h>
#include <wchar.h>
#define MAX_WIDTH 256
#define MAX_HEIGHT 256

void first_part(FILE *input);
void second_part(FILE *input);

int main(int argc, char *argv[]) {
  process_input(argc, argv, first_part, second_part);
}

typedef struct {
  char raw[MAX_WIDTH][MAX_HEIGHT];
  int n_rows;
  int n_cols;
} Map;

typedef struct {
  int i;
  int j;
} Position;

typedef enum { NORTH, WEST, EAST, SOUTH, NO } Direction;

typedef struct {
  Direction d1;
  Direction d2;
} DirectionPipe;

static DirectionPipe shapes[256] = {
    ['|'] = {NORTH, SOUTH}, ['-'] = {EAST, WEST},  ['L'] = {NORTH, EAST},
    ['J'] = {NORTH, WEST},  ['7'] = {SOUTH, WEST}, ['F'] = {SOUTH, EAST},
    ['.'] = {NO, NO}};

static char shape_char[4][4] = {
    [NORTH][SOUTH] = '|', [EAST][WEST] = '-',  [NORTH][EAST] = 'L',
    [NORTH][WEST] = 'J',  [SOUTH][WEST] = '7', [SOUTH][EAST] = 'F'};

int Map_is_in_range(Map *map, Position pos) {
  return pos.i >= 0 && pos.i < map->n_rows && pos.j >= 0 && pos.j < map->n_cols;
}

char Map_char_at_position(Map *map, Position pos) {
  if (Map_is_in_range(map, pos)) {
    return map->raw[pos.i][pos.j];
  }
  return '.';
}

static inline char get_shape_char(Direction d1, Direction d2) {
  char c1 = shape_char[d1][d2];
  char c2 = shape_char[d2][d1];
  // only one combination is defined, the other is 0
  return c1 + c2;
}

Direction Direction_opposite(Direction d) {
  Direction opp;
  switch (d) {
  case NORTH:
    opp = SOUTH;
    break;
  case SOUTH:
    opp = NORTH;
    break;
  case EAST:
    opp = WEST;
    break;
  case WEST:
    opp = EAST;
    break;
  default:
    opp = NO;
  }
  return opp;
}

Position Position_evaluate_direction(Position pos, Direction d) {
  Position new = pos;
  switch (d) {
  case NORTH:
    new.i -= 1;
    break;
  case SOUTH:
    new.i += 1;
    break;
  case EAST:
    new.j += 1;
    break;
  case WEST:
    new.j -= 1;
    break;
  default:
    break;
  }
  return new;
}

char infer_original_shape(Position starting, Map *map) {
  Direction d[2];
  int curr = 0;
  Position candidates[4] = {{starting.i - 1, starting.j},
                            {starting.i + 1, starting.j},
                            {starting.i, starting.j - 1},
                            {starting.i, starting.j + 1}};
  Direction expected_directions[] = {SOUTH, NORTH, EAST, WEST};
  for (int i = 0; i < 4; i++) {
    char pipe_char = Map_char_at_position(map, candidates[i]);
    if (pipe_char != '.') {
      DirectionPipe direction_pipe = shapes[pipe_char];
      if (expected_directions[i] == direction_pipe.d1 ||
          expected_directions[i] == direction_pipe.d2) {
        d[curr] = Direction_opposite(expected_directions[i]);
        curr++;
      }
    }
  }
  return get_shape_char(d[0], d[1]);
}

Position Map_find_initial_position(Map *map) {
  for (int i = 0; i < map->n_rows; i++) {
    for (int j = 0; j < map->n_cols; j++) {
      if (map->raw[i][j] == 'S') {
        Position pos = {i, j};
        map->raw[i][j] = infer_original_shape(pos, map);
        return pos;
      }
    }
  }
  Position invalid = {-1, -1};
  return invalid;
}

DirectionPipe DirectionPipe_get_for_position(Position pos, Map *map) {
  char curr_char = Map_char_at_position(map, pos);
  return shapes[curr_char];
}

Map Map_init() {
  Map m;
  memset(&m, 0, sizeof(m));
  return m;
}

void first_part(FILE *input) {
  Map map = Map_init();
  while (fgets(map.raw[map.n_rows], MAX_WIDTH, input)) {
    map.raw[map.n_rows][strcspn(map.raw[map.n_rows], "\n")] = 0;
    map.n_rows++;
    if (map.n_cols == 0) {
      map.n_cols = strlen(map.raw[0]);
    }
  }
  Position start = Map_find_initial_position(&map);
  Position curr = start;
  DirectionPipe start_directions = DirectionPipe_get_for_position(start, &map);
  Direction direction = start_directions.d1;
  int counter = 0;
  do {
    Position new = Position_evaluate_direction(curr, direction);
    DirectionPipe new_pipe = DirectionPipe_get_for_position(new, &map);
    direction = new_pipe.d1 == Direction_opposite(direction) ? new_pipe.d2
                                                             : new_pipe.d1;
    curr = new;
    counter++;
  } while (curr.i != start.i || curr.j != start.j);

  printf("%d\n", counter / 2 + counter % 2);
}

void second_part(FILE *input) {
  Map map = Map_init();
  while (fgets(map.raw[map.n_rows], MAX_WIDTH, input)) {
    map.raw[map.n_rows][strcspn(map.raw[map.n_rows], "\n")] = 0;
    map.n_rows++;
    if (map.n_cols == 0) {
      map.n_cols = strlen(map.raw[0]);
    }
  }

  Position start = Map_find_initial_position(&map);
  Position curr = start;
  DirectionPipe start_directions = DirectionPipe_get_for_position(start, &map);
  Direction direction = start_directions.d1;
  Map main_loop = Map_init();
  do {
    Position new = Position_evaluate_direction(curr, direction);
    DirectionPipe new_pipe = DirectionPipe_get_for_position(new, &map);
    direction = new_pipe.d1 == Direction_opposite(direction) ? new_pipe.d2
                                                             : new_pipe.d1;

    main_loop.raw[curr.i][curr.j] = Map_char_at_position(&map, curr);
    curr = new;
  } while (curr.i != start.i || curr.j != start.j);

  for (int i = 0; i < map.n_rows; i++) {
    for (int j = 0; j < map.n_cols; j++) {
      char map_char = map.raw[i][j];
      char main_loop_char = main_loop.raw[i][j];
      if (map_char != main_loop_char) {
        map.raw[i][j] = '#';
      }
    }
  }

  int inside_tile_counter = 0;
  int inside_loop = 0;
  char previous_corner;
  for (int i = 0; i < map.n_rows; i++) {
    int intersection_counter = 0;
    for (int j = 0; j < map.n_cols; j++) {
      switch (map.raw[i][j]) {
      case '#':
        if (inside_loop) {
          map.raw[i][j] = 'X';
          inside_tile_counter++;
        }
        break;
      case '|':
        inside_loop = !inside_loop;
        break;
      case 'F':
        previous_corner = 'F';
        break;
      case 'L':
        previous_corner = 'L';
        break;
      case 'J':
        if (previous_corner == 'F') {
          inside_loop = !inside_loop;
        }
        previous_corner = 'J';
        break;
      case '7':
        if (previous_corner == 'L') {
          inside_loop = !inside_loop;
        }
        previous_corner = '7';
        break;
      default:
        break;
      }
    }
  }
  setlocale(LC_CTYPE, "");
  for (int i = 0; i < map.n_rows; i++) {
    for (int j = 0; j < map.n_cols; j++) {
      wchar_t unicode;
      switch (map.raw[i][j]) {
      case 'F':
        unicode = 0x250c;
        break;
      case 'L':
        unicode = 0x2514;
        break;
      case '7':
        unicode = 0x2510;
        break;
      case 'J':
        unicode = 0x2518;
        break;
      case '-':
        unicode = 0x2500;
        break;
      case '|':
        unicode = 0x2502;
        break;
      default:
        unicode = map.raw[i][j];
        break;
      }
      wprintf(L"%lc", unicode);
    }
    wprintf(L"\n");
  }

  wprintf(L"%d\n", inside_tile_counter);
}
