#include "../utils.h"
#include <stdio.h>
#include <string.h>
#define STRINGLEN 512

char input_buffer[STRINGLEN];

static inline int is_digit(char c) {
  if (c >= '0' && c <= '9') {
    return 1;
  }
  return 0;
}

void first_part(FILE *input) {
  int sum = 0;
  int first_digit, second_digit;
  int updated = 0;

  while (fgets(input_buffer, STRINGLEN, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    if (strcmp(input_buffer, "") == 0) {
      break;
    }
    first_digit = 0;
    second_digit = strlen(input_buffer) - 1;

    do {
      updated = 0;
      if (!is_digit(input_buffer[first_digit])) {
        first_digit++;
        updated = 1;
      }

      if (!is_digit(input_buffer[second_digit])) {
        second_digit--;
        updated = 1;
      }

    } while (first_digit != second_digit && updated);

    sum += 10 * (input_buffer[first_digit] - '0') + input_buffer[second_digit] -
           '0';
  }
  printf("%d\n", sum);
}

int get_digit(char *start, char **digits, int digit_len) {
  if (is_digit(start[0])) {
    return start[0] - '0';
  }

  for (int i = 0; i < digit_len; i++) {
    if (strlen(start) < strlen(digits[i])) {
      continue;
    }
    int result = memcmp(start, digits[i], strlen(digits[i]));
    if (result == 0) {
      return i + 1;
    }
  }
  return -1;
}

void second_part(FILE *input) {
  char *digits[] = {"one", "two",   "three", "four", "five",
                    "six", "seven", "eight", "nine"};
  int start_offset, end_offset;
  int sum = 0;

  while (fgets(input_buffer, STRINGLEN, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    if (strcmp(input_buffer, "") == 0) {
      break;
    }
    int first_digit = -1, second_digit = -1;
    start_offset = 0;
    end_offset = strlen(input_buffer) - 1;

    do {
      int digit;
      if (first_digit < 0) {
        digit = get_digit(input_buffer + start_offset, digits,
                          (sizeof digits / sizeof digits[0]));

        if (digit < 0) {
          start_offset++;
        } else {
          first_digit = digit;
        }
      }

      if (second_digit < 0) {
        digit = get_digit(input_buffer + end_offset, digits,
                          (sizeof digits / sizeof digits[0]));
        if (digit < 0) {
          end_offset--;
        } else {
          second_digit = digit;
        }
      }

    } while (first_digit < 0 || second_digit < 0);

    sum += first_digit * 10 + second_digit;
  }

  printf("%d\n", sum);
}

int main(int argc, char *argv[]) {
  process_input(argc, argv, first_part, second_part);
}
