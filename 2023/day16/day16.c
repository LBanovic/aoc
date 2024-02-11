#include "../structs/fixed_array.h"
#include "../utils.h"
#include <stdio.h>
#include <string.h>

void first_part(FILE *input);
void second_part(FILE *input);

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}

#define INPUT_BUFFER_SIZE 256
#define MAX_POSITION_COUNT 1000

typedef enum {
  Direction_UP = 1,
  Direction_DOWN = 2,
  Direction_LEFT = 4,
  Direction_RIGHT = 8
} Direction;

typedef struct {
  int i;
  int j;
  Direction direction;
} Position;

typedef struct {
  Position items[MAX_POSITION_COUNT];
  size_t size;
} Positions;

void Positions_add(Positions *positions, Position position) {
  fixed_array_append(positions, position);
}

Position Positions_pop(Positions *positions) {
  Position p;
  fixed_array_pop(positions, 0, &p);
  return p;
}

typedef struct {
  char spaces[INPUT_BUFFER_SIZE][INPUT_BUFFER_SIZE];
  int visited[INPUT_BUFFER_SIZE][INPUT_BUFFER_SIZE];
  size_t n_rows;
  size_t n_cols;
} Map;

int Position_is_valid(Position p, Map *map) {
  return p.i >= 0 && p.i < map->n_rows && p.j >= 0 && p.j < map->n_cols;
}

void Map_update(Map *map, Positions *current) {
  Position pos = Positions_pop(current);
  if (!Position_is_valid(pos, map) ||
      (map->visited[pos.i][pos.j] & pos.direction)) {
    return;
  }
  char space = map->spaces[pos.i][pos.j];
  map->visited[pos.i][pos.j] |= pos.direction;
  switch (space) {
  case '-':
    if (pos.direction == Direction_LEFT || pos.direction == Direction_RIGHT) {
      break;
    } else {
      Position new_pos = pos;
      new_pos.direction = Direction_LEFT;
      pos.direction = Direction_RIGHT;
      Positions_add(current, new_pos);
    }
    break;
  case '|':
    if (pos.direction == Direction_UP || pos.direction == Direction_DOWN) {
      break;
    } else {
      Position new_pos = pos;
      new_pos.direction = Direction_UP;
      pos.direction = Direction_DOWN;
      Positions_add(current, new_pos);
    }
    break;
  case '/':
    // LEFT <-> DOWN, RIGHT <-> UP
    pos.direction = 8 / pos.direction;
    break;
  case '\\':
    // LEFT <-> UP, RIGHT <-> DOWN
    {
      int num_shifted = pos.direction << 2;
      pos.direction = num_shifted > 8 ? num_shifted / 16 : num_shifted;
    }
    break;
  default:
    break;
  }

  switch (pos.direction) {
  case Direction_UP:
    pos.i -= 1;
    break;
  case Direction_DOWN:
    pos.i += 1;
    break;
  case Direction_RIGHT:
    pos.j += 1;
    break;
  case Direction_LEFT:
    pos.j -= 1;
    break;
  }
  Positions_add(current, pos);
}

void first_part(FILE *input) {
  Map map = {0};
  Position starting = {0, 0, Direction_RIGHT};
  Positions current = {0};
  Positions_add(&current, starting);

  while (fgets(map.spaces[map.n_rows], INPUT_BUFFER_SIZE, input)) {
    char *curr_row = map.spaces[map.n_rows];
    curr_row[strcspn(curr_row, "\n")] = 0;
    map.n_rows++;
  }
  map.n_cols = strnlen(map.spaces[0], INPUT_BUFFER_SIZE);

  do {
    Map_update(&map, &current);
  } while (current.size > 0);

  int sum = 0;
  for (int i = 0; i < map.n_rows; i++) {
    for (int j = 0; j < map.n_cols; j++) {
      sum += (map.visited[i][j] > 0);
    }
  }

  printf("%d\n", sum);
}

int get_n_energized(Map map, Position starting) {
  Positions current = {0};
  Positions_add(&current, starting);
  do {
    Map_update(&map, &current);
  } while (current.size > 0);

  int sum = 0;
  for (int i = 0; i < map.n_rows; i++) {
    for (int j = 0; j < map.n_cols; j++) {
      sum += (map.visited[i][j] > 0);
    }
  }

  return sum;
}

void second_part(FILE *input) {
  Map map = {0};

  while (fgets(map.spaces[map.n_rows], INPUT_BUFFER_SIZE, input)) {
    char *curr_row = map.spaces[map.n_rows];
    curr_row[strcspn(curr_row, "\n")] = 0;
    map.n_rows++;
  }
  map.n_cols = strnlen(map.spaces[0], INPUT_BUFFER_SIZE);

  int max_val = 0;
  for (int i = 0; i < map.n_rows; i++) {
    Position right = {i, 0, Direction_RIGHT};
    int curr_val = get_n_energized(map, right);
    max_val = max_val < curr_val ? curr_val : max_val;

    Position left = {i, map.n_cols - 1, Direction_LEFT};
    curr_val = get_n_energized(map, left);
    max_val = max_val < curr_val ? curr_val : max_val;
  }

  for (int i = 0; i < map.n_cols; i++) {
    Position down = {0, i, Direction_DOWN};
    int curr_val = get_n_energized(map, down);
    max_val = max_val < curr_val ? curr_val : max_val;

    Position up = {map.n_rows - 1, i, Direction_UP};
    curr_val = get_n_energized(map, up);
    max_val = max_val < curr_val ? curr_val : max_val;
  }

  printf("%d\n", max_val);
}
