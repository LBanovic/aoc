#include "../utils.h"
#include <assert.h>
#include <stdio.h>
#define SCHEMATIC_SIZE 140
#define LINE_SIZE SCHEMATIC_SIZE + 2
#define ARRLEN(arr) (sizeof(arr) / sizeof(arr[0]))

char input_buffer[SCHEMATIC_SIZE][LINE_SIZE];

static inline int is_digit(char c) {

  if (!(c >= '0' && c <= '9')) {
    return 0;
  }
  return 1;
}

static inline int as_digit(char c) {
  if (!is_digit(c)) {
    return -1;
  }
  return c - '0';
}

static inline int is_symbol(int row, int col) {
  if (!(row >= 0 && row < SCHEMATIC_SIZE) ||
      !(col >= 0 && col < SCHEMATIC_SIZE)) {
    return 0;
  }
  char c = input_buffer[row][col];
  return !is_digit(c) && c != '.';
}

static inline int is_near_symbol(int row, int col) {
  for (int i = -1; i < 2; i++) {
    int curr_row = row + i;
    for (int j = -1; j < 2; j++) {
      int curr_col = col + j;
      if (curr_col == col && curr_row == row) {
        continue;
      }
      if (is_symbol(curr_row, curr_col)) {
        return 1;
      }
    }
  }
  return 0;
}

void first_part(FILE *input) {
  for (int i = 0; i < SCHEMATIC_SIZE; i++) {
    char *res = fgets(input_buffer[i], LINE_SIZE, input);
    assert(res != NULL);
  }

  int sum = 0;
  int near_symbol = 0;

  for (int i = 0; i < ARRLEN(input_buffer); i++) {
    int current_num = 0;
    for (int j = 0; j < LINE_SIZE; j++) {
      int d = as_digit(input_buffer[i][j]);
      near_symbol = (d >= 0) && is_near_symbol(i, j) || near_symbol;
      if (d < 0) {
        if (near_symbol) {
          sum += current_num;
        }
        near_symbol = 0;
        current_num = 0;
        continue;
      }
      current_num = current_num * 10 + d;
    }
  }

  printf("%d\n", sum);
}

typedef struct {
  int x1;
  int x2;
  int y;
} NumberPosition;

typedef struct {
  int number;
  NumberPosition position;
} Number;

inline static int is_neighbour(int x, int y, NumberPosition pos) {
  for (int x1 = pos.x1; x1 < pos.x2; x1++) {
    if (x >= x1 - 1 && x <= x1 + 1 && y >= pos.y - 1 && y <= pos.y + 1) {
      return 1;
    }
  }
  return 0;
}

void second_part(FILE *input) {
  for (int i = 0; i < SCHEMATIC_SIZE; i++) {
    char *res = fgets(input_buffer[i], LINE_SIZE, input);
    assert(res != NULL);
  }

  Number numbers[SCHEMATIC_SIZE * SCHEMATIC_SIZE] = {0};
  Number gear_neighbours[SCHEMATIC_SIZE * SCHEMATIC_SIZE][2] = {0};
  int sum = 0;
  int number_of_detected_numbers = 0;
  int number_of_gears = 0;

  for (int i = 0; i < ARRLEN(input_buffer); i++) {
    Number current_num = {.number = 0, .position = {-1, -1, -1}};
    for (int j = 0; j < SCHEMATIC_SIZE; j++) {
      int d = as_digit(input_buffer[i][j]);
      if (d < 0) {
        if (current_num.number > 0) {
          Number next_num = {.number = 0, .position = {-1, -1, -1}};
          numbers[number_of_detected_numbers] = current_num;
          number_of_detected_numbers++;
          current_num = next_num;
        }
        continue;
      }
      current_num.number = current_num.number * 10 + d;
      if (current_num.position.x1 < 0) {
        current_num.position.x1 = j;
      }
      current_num.position.x2 = j + 1;
      current_num.position.y = i;
    }
    if (current_num.number > 0) {
      Number next_num = {.number = 0, .position = {-1, -1, -1}};
      numbers[number_of_detected_numbers] = current_num;
      number_of_detected_numbers++;
      current_num = next_num;
    }
  }

  Number empty_num = {0};
  for (int i = 0; i < ARRLEN(input_buffer); i++) {
    for (int j = 0; j < SCHEMATIC_SIZE; j++) {
      if (input_buffer[i][j] == '*') {
        int current = 0;
        for (int k = 0; k < number_of_detected_numbers; k++) {
          if (is_neighbour(j, i, numbers[k].position)) {
            if (current > 1) {
              gear_neighbours[number_of_gears][0] = empty_num;
              gear_neighbours[number_of_gears][1] = empty_num;
              break;
            }
            gear_neighbours[number_of_gears][current] = numbers[k];
            current++;
          }
        }
        number_of_gears++;
      }
    }
  }

  for (int i = 0; i < number_of_gears + 1; i++) {
    sum = sum + gear_neighbours[i][0].number * gear_neighbours[i][1].number;
  }
  printf("%d\n", sum);
}

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}
