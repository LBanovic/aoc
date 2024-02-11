#include "../utils.h"
#include <stdlib.h>
#include <string.h>
#define BUFFER_SIZE 512
#define NUMBER_BUFSIZE 100

char input_buffer[BUFFER_SIZE];

void first_part(FILE *input);
void second_part(FILE *input);

typedef int elemtype;

typedef struct {
  elemtype numbers[NUMBER_BUFSIZE];
  int size;
} NumberArr;

NumberArr NumberArr_init() {
  NumberArr arr;
  memset(&arr, 0, sizeof(arr));
  return arr;
}

NumberArr NumberArr_load_from_line(char *input) {
  NumberArr arr = NumberArr_init();

  char *split = strtok(input, " ");
  while (split != NULL) {
    arr.numbers[arr.size] = strtol(split, NULL, 10);
    arr.size++;
    split = strtok(NULL, " ");
  }
  return arr;
}

NumberArr NumberArr_first_order_difference(NumberArr *arr) {
  NumberArr new_arr = NumberArr_init();
  for (int i = 1; i < arr->size; i++) {
    new_arr.numbers[new_arr.size] = arr->numbers[i] - arr->numbers[i - 1];
    new_arr.size++;
  }
  return new_arr;
}

int NumberArr_is_all_eq(NumberArr *arr, elemtype cmp) {
  for (int i = 0; i < arr->size; i++) {
    if (arr->numbers[i] != cmp) {
      return 0;
    }
  }
  return 1;
}

elemtype NumberArr_resolve(NumberArr *number_arr) {
  if (NumberArr_is_all_eq(number_arr, 0)) {
    return 0;
  }
  NumberArr newArr = NumberArr_first_order_difference(number_arr);
  return number_arr->numbers[number_arr->size - 1] + NumberArr_resolve(&newArr);
}

int main(int argc, char *argv[]) {
  process_input(argc, argv, first_part, second_part);
}

void first_part(FILE *input) {
  elemtype sum = 0;
  while (fgets(input_buffer, BUFFER_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    NumberArr arr = NumberArr_load_from_line(input_buffer);
    sum += NumberArr_resolve(&arr);
  }
  printf("%d\n", sum);
}

elemtype NumberArr_resolve_first_elem(NumberArr *number_arr) {
  if (NumberArr_is_all_eq(number_arr, 0)) {
    return 0;
  }
  NumberArr newArr = NumberArr_first_order_difference(number_arr);
  elemtype x = number_arr->numbers[0] - NumberArr_resolve_first_elem(&newArr);
  return x;
}
void second_part(FILE *input) {
  elemtype sum = 0;
  while (fgets(input_buffer, BUFFER_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    NumberArr arr = NumberArr_load_from_line(input_buffer);
    elemtype x = NumberArr_resolve_first_elem(&arr);
    sum += x;
  }
  printf("%d\n", sum);
}
