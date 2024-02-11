#include "../utils.h"
#include <stdio.h>
#include <string.h>
#define INPUT_BUFFER_SIZE 256

void first_part(FILE *input);
void second_part(FILE *input);

char input_buffer[INPUT_BUFFER_SIZE];

typedef struct {
  int row;
  int col;
} Point;

typedef struct {
  Point galaxies[INPUT_BUFFER_SIZE * INPUT_BUFFER_SIZE];
  int size;
} Points;

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}

void first_part(FILE *input) {
  Points points;
  memset(&points, 0, sizeof(points));

  int empty_rows[INPUT_BUFFER_SIZE];
  memset(empty_rows, 1, sizeof(empty_rows));

  int empty_cols[INPUT_BUFFER_SIZE];
  memset(empty_cols, 1, sizeof(empty_cols));

  int row_num = 0;
  while (fgets(input_buffer, INPUT_BUFFER_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;

    for (int i = 0; i < strlen(input_buffer); i++) {
      if (input_buffer[i] == '#') {
        empty_rows[row_num] = 0;
        empty_cols[i] = 0;
        points.galaxies[points.size].row = row_num;
        points.galaxies[points.size].col = i;
        points.size++;
      }
    }
    row_num++;
  }

  Points backup_points;
  memcpy(&backup_points, &points, sizeof(points));

  for (int i = 0; i < INPUT_BUFFER_SIZE; i++) {
    if (empty_rows[i]) {
      for (int j = 0; j < points.size; j++) {
        if (points.galaxies[j].row > i) {
          backup_points.galaxies[j].row++;
        }
      }
    }
  }

  for (int i = 0; i < INPUT_BUFFER_SIZE; i++) {
    if (empty_cols[i]) {
      for (int j = 0; j < points.size; j++) {
        if (points.galaxies[j].col > i) {
          backup_points.galaxies[j].col++;
        }
      }
    }
  }

  int sum = 0;
  for (int i = 0; i < backup_points.size; i++) {
    Point p1 = backup_points.galaxies[i];
    for (int j = i + 1; j < backup_points.size; j++) {
      Point p2 = backup_points.galaxies[j];
      sum += abs(p1.row - p2.row) + abs(p1.col - p2.col);
    }
  }

  printf("%d\n", sum);
}

#define INCREMENT 1000000

void second_part(FILE *input) {
  Points points;
  memset(&points, 0, sizeof(points));

  int empty_rows[INPUT_BUFFER_SIZE];
  memset(empty_rows, 1, sizeof(empty_rows));

  int empty_cols[INPUT_BUFFER_SIZE];
  memset(empty_cols, 1, sizeof(empty_cols));

  int row_num = 0;
  while (fgets(input_buffer, INPUT_BUFFER_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;

    for (int i = 0; i < strlen(input_buffer); i++) {
      if (input_buffer[i] == '#') {
        empty_rows[row_num] = 0;
        empty_cols[i] = 0;
        points.galaxies[points.size].row = row_num;
        points.galaxies[points.size].col = i;
        points.size++;
      }
    }
    row_num++;
  }

  Points backup_points;
  memcpy(&backup_points, &points, sizeof(points));

  for (int i = 0; i < INPUT_BUFFER_SIZE; i++) {
    if (empty_rows[i]) {
      for (int j = 0; j < points.size; j++) {
        if (points.galaxies[j].row > i) {
          backup_points.galaxies[j].row += INCREMENT - 1;
        }
      }
    }
  }

  for (int i = 0; i < INPUT_BUFFER_SIZE; i++) {
    if (empty_cols[i]) {
      for (int j = 0; j < points.size; j++) {
        if (points.galaxies[j].col > i) {
          backup_points.galaxies[j].col += INCREMENT - 1;
        }
      }
    }
  }

  long sum = 0;
  for (int i = 0; i < backup_points.size; i++) {
    Point p1 = backup_points.galaxies[i];
    for (int j = i + 1; j < backup_points.size; j++) {
      Point p2 = backup_points.galaxies[j];
      sum += abs(p1.row - p2.row) + abs(p1.col - p2.col);
    }
  }

  printf("%ld\n", sum);
}
