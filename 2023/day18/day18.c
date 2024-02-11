#include "../utils.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_DIG_STEPS 800
#define INPUT_BUFFER_SIZE 256

typedef struct {
  int direction_x;
  int direction_y;
  long value;
  char hex_code[7];
} DigStep;

DigStep DigStep_parse(char *line) {
  char delimiters[] = " ()\n#";
  char *split = strtok(line, delimiters);
  DigStep step = {0};
  int part = 0;
  while (split != NULL) {
    if (part == 0) {
      switch (split[0]) {
      case 'U':
        step.direction_x = 0;
        step.direction_y = -1;
        break;
      case 'D':
        step.direction_x = 0;
        step.direction_y = 1;
        break;
      case 'R':
        step.direction_x = 1;
        step.direction_y = 0;
        break;
      case 'L':
        step.direction_x = -1;
        step.direction_y = 0;
        break;
      default:
        assert(0);
        break;
      }
    } else if (part == 1) {
      step.value = strtol(split, NULL, 10);
    } else {
      strncpy(step.hex_code, split, sizeof(step.hex_code));
    }
    split = strtok(NULL, delimiters);
    part++;
  }
  return step;
}

typedef struct {
  DigStep elements[MAX_DIG_STEPS];
  size_t size;
} List;

void List_add(List *list, DigStep step) {
  list->elements[list->size] = step;
  list->size++;
}

typedef struct {
  long x;
  long y;
} Point;

char input_buffer[INPUT_BUFFER_SIZE] = {0};

void first_part(FILE *input) {
  List list = {0};
  while (fgets(input_buffer, sizeof(input_buffer), input)) {
    DigStep step = DigStep_parse(input_buffer);
    List_add(&list, step);
  }

  Point curr_point = {0, 0};
  long sum = 0;
  long remainder = 0;
  for (int i = 0; i < list.size; i++) {
    Point prev_point = curr_point;
    DigStep step = list.elements[i];
    curr_point.x += step.direction_x * step.value;
    curr_point.y += step.direction_y * step.value;
    sum += prev_point.x * curr_point.y - prev_point.y * curr_point.x;
    remainder += step.value;
  }
  printf("%ld\n", (sum + remainder) / 2 + 1);
}

DigStep DigStep_parse_hexa(char *input) {
  DigStep step = DigStep_parse(input);
  switch (step.hex_code[5]) {
  case '0':
    step.direction_x = 1;
    step.direction_y = 0;
    break;
  case '1':
    step.direction_x = 0;
    step.direction_y = 1;
    break;
  case '2':
    step.direction_x = -1;
    step.direction_y = 0;
    break;
  case '3':
    step.direction_x = 0;
    step.direction_y = -1;
    break;
  }
  step.hex_code[5] = 0;
  step.value = strtol(step.hex_code, NULL, 16);
  return step;
}

void second_part(FILE *input) {
  List list = {0};
  while (fgets(input_buffer, sizeof(input_buffer), input)) {
    DigStep step = DigStep_parse_hexa(input_buffer);
    List_add(&list, step);
  }

  Point curr_point = {0, 0};
  long sum = 0;
  long remainder = 0;
  for (int i = 0; i < list.size; i++) {
    Point prev_point = curr_point;
    DigStep step = list.elements[i];
    curr_point.x += step.direction_x * step.value;
    curr_point.y += step.direction_y * step.value;
    sum += prev_point.x * curr_point.y - prev_point.y * curr_point.x;
    remainder += step.value;
  }
  printf("%ld\n", (sum + remainder) / 2 + 1);
}

int main(int argc, char *argv[]) {
  process_input(argc, argv, first_part, second_part);
}
