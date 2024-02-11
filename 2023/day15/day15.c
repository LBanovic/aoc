#include "../utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void first_part(FILE *input);
void second_part(FILE *input);

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}

void first_part(FILE *input) {
  char c;
  int sum = 0;
  int current_value = 0;
  while (1) {
    c = fgetc(input);
    if (c == ',' || c == EOF || c == '\n') {
      sum += current_value;
      current_value = 0;
    } else {
      current_value += c;
      current_value *= 17;
      current_value %= 256;
    }
    if (c == EOF || c == '\n') {
      break;
    }
  }
  printf("%d\n", sum);
}

#define MAX_BOX_SIZE 128
#define MAX_LABEL_LEN 8
#define NUM_BOXES 256
#define INPUT_BUFSIZE 1048576

int hash(char *str) {
  int num = 0;
  for (int i = 0; i < strlen(str); i++) {
    num += str[i];
    num *= 17;
    num %= 256;
  }
  return num;
}

typedef struct {
  char labels[MAX_BOX_SIZE][MAX_LABEL_LEN];
  int focal_lens[MAX_BOX_SIZE];
  size_t size;
} Box;

static Box HashMap[NUM_BOXES] = {0};
static char input_buffer[INPUT_BUFSIZE] = {0};

int Box_index_of(Box *box, char *label) {
  for (int i = 0; i < box->size; i++) {
    if (strcmp(box->labels[i], label) == 0) {
      return i;
    }
  }
  return -1;
}

void Box_add_or_update(Box *box, char *label, int focal) {
  int index_of_label = Box_index_of(box, label);
  if (index_of_label >= 0) {
    box->focal_lens[index_of_label] = focal;
  } else {
    strcpy(box->labels[box->size], label);
    box->focal_lens[box->size] = focal;
    box->size++;
  }
}

void Box_delete(Box *box, char *label) {
  int index_of_label = Box_index_of(box, label);
  if (index_of_label >= 0) {
    memmove(box->labels[index_of_label], box->labels[index_of_label + 1],
            (box->size - index_of_label - 1) * sizeof(box->labels[0]));
    memmove(box->focal_lens + index_of_label,
            box->focal_lens + index_of_label + 1,
            (box->size - index_of_label - 1) * sizeof(int));
    box->size--;
  }
}

void Box_print(Box *box) {
  for (int i = 0; i < box->size; i++) {
    printf("[%s %d] ", box->labels[i], box->focal_lens[i]);
  }
}

typedef enum { Type_Char, Type_Digit } Type;

Type digit_or_char(char c) {
  if (c >= '0' && c <= '9') {
    return Type_Digit;
  }
  return Type_Char;
}

void second_part(FILE *input) {
  fgets(input_buffer, INPUT_BUFSIZE, input);
  char *label;
  int label_len;

  char delimiters[] = "=,";
  char *split = strtok(input_buffer, delimiters);
  int index;
  while (split != NULL) {
    switch (digit_or_char(split[0])) {
    case Type_Char:
      label = split;
      label_len = strlen(label);
      if (label[label_len - 1] == '-') {
        label[label_len - 1] = 0;
        index = hash(label);
        Box *box = &HashMap[index];
        Box_delete(box, label);
      }
      break;
    case Type_Digit:
      index = hash(label);
      Box *box = &HashMap[index];
      Box_add_or_update(box, label, strtol(split, NULL, 10));
      break;
    }
    split = strtok(NULL, delimiters);
  }

  int sum = 0;
  for (int i = 0; i < NUM_BOXES; i++) {
    for (int j = 0; j < HashMap[i].size; j++) {
      sum += (i + 1) * (j + 1) * HashMap[i].focal_lens[j];
    }
  }
  printf("%d\n", sum);
}
