#include "../utils.h"
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define INPUT_SIZE 512
#define MAX(a, b) ((a) >= (b) ? (a) : (b))

#define R_LIMIT 12
#define G_LIMIT 13
#define B_LIMIT 14

char input_buffer[INPUT_SIZE];

typedef struct {
  int red;
  int green;
  int blue;
} Round;

void first_part(FILE *input) {
  int sum = 0;

  while (fgets(input_buffer, INPUT_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    Round r = {.red = 0, .green = 0, .blue = 0};
    char *modified = strtok(input_buffer, " ,;:");
    int current_num;
    int gameid = -1;

    while (modified != NULL) {
      switch (modified[0]) {
      case 'G': // Game
        break;
      case 'b': // blue
        r.blue = MAX(current_num, r.blue);
        break;
      case 'g': // green
        r.green = MAX(current_num, r.green);
        break;
      case 'r': // red
        r.red = MAX(current_num, r.red);
        break;
      default:
        current_num = strtol(modified, NULL, 10);
        if (gameid < 0) {
          gameid = current_num;
        }
      }

      modified = strtok(NULL, " ,;:");
    }

    if (r.green <= G_LIMIT && r.red <= R_LIMIT && r.blue <= B_LIMIT) {
      sum += gameid;
    }
  }

  printf("%d\n", sum);
}

void second_part(FILE *input) {
  int sum = 0;

  while (fgets(input_buffer, INPUT_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    Round r = {.red = 0, .green = 0, .blue = 0};
    char *modified = strtok(input_buffer, " ,;:");
    int current_num;

    while (modified != NULL) {
      switch (modified[0]) {
      case 'G': // Game
        break;
      case 'b': // blue
        r.blue = MAX(current_num, r.blue);
        break;
      case 'g': // green
        r.green = MAX(current_num, r.green);
        break;
      case 'r': // red
        r.red = MAX(current_num, r.red);
        break;
      default:
        current_num = strtol(modified, NULL, 10);
        if (errno == ERANGE) {
          printf("Failed to convert!\n");
        }
      }
      modified = strtok(NULL, " ,;:");
    }

    sum += r.blue * r.green * r.red;
  }

  printf("%d\n", sum);
}

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}
