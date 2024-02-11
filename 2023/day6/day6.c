#include "../utils.h"
#include <math.h>
#include <stdio.h>
#include <string.h>
#define INPUT_BUFFER_SIZE 128

char input_buffer[INPUT_BUFFER_SIZE];

int get_number_of_solutions(long time, long distance);

void first_part(FILE *input) {
  int time[4] = {0};
  int distance[4] = {0};
  int line_index = 0;
  int n_pairs;
  while (fgets(input_buffer, INPUT_BUFFER_SIZE, input)) {
    char *split = strtok(input_buffer, " \t");
    int num;
    n_pairs = 0;
    while (split != NULL) {
      printf("%s\n", split);
      switch (split[0]) {
      case 'T':
        break;
      case 'D':
        break;
      default:
        num = strtol(split, NULL, 10);
        if (line_index == 0) {
          time[n_pairs] = num;
        } else {
          distance[n_pairs] = num;
        }
        n_pairs++;
      }
      split = strtok(NULL, " ");
    }
    line_index++;
  }
  printf("N_PAIRS %d\n", n_pairs);
  for (int i = 0; i < n_pairs; i++) {
    fprintf(stderr, "time %d, distance %d\n", time[i], distance[i]);
  }

  int prod = 1;
  for (int i = 0; i < n_pairs; i++) {
    int x = get_number_of_solutions(time[i], distance[i]);
    prod *= x;
    printf("%d\n", x);
  }

  printf("%d\n", prod);
}

int get_number_of_solutions(long time, long distance) {
  /* finding number of whole numbers between roots of quadratic x(t-x) = d
   *
   * Reformulated, it is -x^2 + tx - d = 0
   *
   * */

  double t = (double)time;
  double d = (double)distance;
  double num1 = -t + sqrt(t * t - 4 * d);
  double num2 = -t - sqrt(t * t - 4 * d);

  double denom = -2;

  double x1 = num1 / denom, x2 = num2 / denom;

  int x1_i = (int)x1 + 1;
  int x2_i = (int)x2;

  if (fabs(x2_i - x2) < 1e-10) {
    x2_i--;
  }

  printf("[%f, %f]\n", x1, x2);
  return (int)(x2_i - x1_i + 1);
}

void second_part(FILE *input) {
  char time[20] = {0};
  char distance[20] = {0};

  int line_index = 0;
  int n_pairs;
  while (fgets(input_buffer, INPUT_BUFFER_SIZE, input)) {
    int current_line_pos = 0;
    for (int i = 0; i < strlen(input_buffer); i++) {
      if (input_buffer[i] >= '0' && input_buffer[i] <= '9') {
        (line_index == 0 ? time : distance)[current_line_pos] = input_buffer[i];
        current_line_pos++;
      }
    }
    line_index++;
  }

  unsigned long total_time = strtoul(time, NULL, 10);
  unsigned long total_distance = strtoul(distance, NULL, 10);

  printf("Total time %ld, Total Distance %ld\n", total_time, total_distance);
  printf("%d\n", get_number_of_solutions(total_time, total_distance));
}

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}
