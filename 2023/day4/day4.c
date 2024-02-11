#include "../utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void first_part(FILE *input);
void second_part(FILE *input);

int main(int argc, char *argv[]) {
  process_input(argc, argv, first_part, second_part);
}

#define INPUT_BUFFER_SIZE 256
#define NUMBER_BUFFER_SIZE 32
char input_buffer[INPUT_BUFFER_SIZE] = {0};

typedef struct {
  int capacity;
  int numbers[NUMBER_BUFFER_SIZE];
} ScratchpadBuffer;

ScratchpadBuffer scratchpad_init() {
  ScratchpadBuffer buf;
  buf.capacity = 0;
  return buf;
}

void first_part(FILE *input) {
  int sum = 0;
  char delimiters[] = ": ";
  while (fgets(input_buffer, INPUT_BUFFER_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    ScratchpadBuffer query_buf = scratchpad_init();
    ScratchpadBuffer search_buf = scratchpad_init();

    int is_search = 0;
    int field_counter = 0;
    char *split = strtok(input_buffer, delimiters);
    int num;
    while (split != NULL) {
      switch (split[0]) {
      case 'C':
        field_counter++;
        break;
      case '|':
        field_counter++;
        is_search = 1;
        break;
      default:
        field_counter++;
        if (field_counter > 2) {
          num = strtol(split, NULL, 10);
          if (is_search) {
            query_buf.numbers[query_buf.capacity] = num;
            query_buf.capacity++;
          } else {
            search_buf.numbers[search_buf.capacity] = num;
            search_buf.capacity++;
          }
        }
      }
      split = strtok(NULL, delimiters);
    }

    int adding = 0;
    for (int i = 0; i < query_buf.capacity; i++) {
      for (int j = 0; j < search_buf.capacity; j++) {
        if (query_buf.numbers[i] == search_buf.numbers[j]) {
          if (adding == 0) {
            adding = 1;
          } else {
            adding *= 2;
          }
        }
      }
    }
    sum += adding;
  }
  printf("%d\n", sum);
}

typedef struct {
  ScratchpadBuffer query;
  ScratchpadBuffer search;
} ScratchCard;

ScratchCard ScratchCard_init() {
  ScratchCard card;
  card.query = scratchpad_init();
  card.search = scratchpad_init();
  return card;
}

#define SCRATCH_CARD_SIZE 200

void second_part(FILE *input) {
  int result[SCRATCH_CARD_SIZE] = {0};
  int number_of_cards = 0;
  while (fgets(input_buffer, INPUT_BUFFER_SIZE, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    char delimiters[] = ": ";

    ScratchCard card = ScratchCard_init();
    char *split = strtok(input_buffer, delimiters);
    int is_search = 0;
    int field_counter = 0;
    while (split != NULL) {
      switch (split[0]) {
      case 'C':
        field_counter++;
        break;
      case '|':
        is_search = 1;
        field_counter++;
      default:
        field_counter++;
        if (field_counter > 2) {
          if (is_search) {
            card.search.numbers[card.search.capacity] = strtol(split, NULL, 10);
            card.search.capacity++;
          } else {
            card.query.numbers[card.query.capacity] = strtol(split, NULL, 10);
            card.query.capacity++;
          }
        }
      }
      split = strtok(NULL, delimiters);
    }
    result[number_of_cards]++;
    int next_lines = 0;
    for (int i = 0; i < card.query.capacity; i++) {
      for (int j = 0; j < card.search.capacity; j++) {
        if (card.query.numbers[i] == card.search.numbers[j]) {
          next_lines++;
          break;
        }
      }
    }
    for (int i = 1; i <= next_lines; i++) {
      result[number_of_cards + i] += result[number_of_cards];
    }
    number_of_cards++;
  }

  int sum = 0;
  for (int i = 0; i < SCRATCH_CARD_SIZE; i++) {
    sum += result[i];
  }
  printf("%d\n", sum);
}
