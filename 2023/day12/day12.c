#include "../utils.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_NUMS 100
#define MAX_SPRINGS 250
#define INPUT_BUFFER_SIZE 128

void first_part(FILE *input);
void second_part(FILE *input);

char input_buffer[INPUT_BUFFER_SIZE] = {0};

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}

typedef struct {
  int numbers[MAX_NUMS];
  int size;
} VerificationCode;

typedef struct {
  char layout[MAX_SPRINGS];
  int unknown_spots[MAX_SPRINGS];
  int size;
  int n_unknown;
} Springs;

VerificationCode VerificationCode_parse(char *input) {
  VerificationCode code = {0};

  char *split = strtok(input, ",");
  while (split != NULL) {
    code.numbers[code.size] = strtol(split, NULL, 10);
    code.size++;
    split = strtok(NULL, ",");
  }
  return code;
}

Springs Springs_parse(char *input) {
  Springs springs = {0};
  memcpy(springs.layout, input, strnlen(input, sizeof(springs.layout)));
  springs.size = strlen(springs.layout);
  for (int i = 0; i < springs.size; i++) {
    if (springs.layout[i] == '?') {
      springs.unknown_spots[springs.n_unknown] = i;
      springs.n_unknown++;
    }
  }
  return springs;
}

typedef struct {
  Springs *springs;
  VerificationCode *code;
  long *result;
  size_t size;
} FunctionCache;

long count_arangements(Springs springs, VerificationCode code,
                       FunctionCache *cache) {
  long res = -1;
  for (int i = 0; i < cache->size; i++) {
    if (memcmp(&(cache->springs[i]), &springs, sizeof(Springs)) == 0 &&
        memcmp(&(cache->code[i]), &code, sizeof(VerificationCode)) == 0) {
      res = cache->result[i];
      break;
    }
  }
  if (res >= 0) {
    return res;
  }

  if (code.size == 0) {
    for (int i = 0; i < springs.size; i++) {
      if (springs.layout[i] == '#') {
        return 0;
      }
    }
    return 1;
  }

  if (springs.size == 0) {
    return 0;
  }

  long result = 0;
  char considering = springs.layout[0];
  if (considering == '.' || considering == '?') {
    Springs new_springs;
    memcpy(new_springs.layout, springs.layout + 1, sizeof(springs.layout) - 1);
    new_springs.size = springs.size - 1;
    result += count_arangements(new_springs, code, cache);
  }

  if (considering == '?' || considering == '#') {
    int is_dot_present = 0;
    for (int i = 0; i < code.numbers[0]; i++) {
      if (springs.layout[i] == '.') {
        is_dot_present = 1;
        break;
      }
    }

    if (code.numbers[0] <= springs.size && !is_dot_present &&
        (code.numbers[0] == springs.size ||
         springs.layout[code.numbers[0]] != '#')) {

      Springs new_springs;
      int offset = code.numbers[0] + 1;
      memcpy(new_springs.layout, springs.layout + offset,
             sizeof(springs.layout) - offset);
      new_springs.size = springs.size - offset;

      VerificationCode new_code;
      memcpy(new_code.numbers, code.numbers + 1,
             sizeof(code.numbers) - sizeof(code.numbers[0]));
      new_code.size = code.size - 1;

      result += count_arangements(new_springs, new_code, cache);
    }
  }

  cache->springs[cache->size] = springs;
  cache->code[cache->size] = code;
  cache->result[cache->size] = result;
  cache->size++;

  return result;
}

FunctionCache *FunctionCache_init(size_t size) {
  FunctionCache *cache = malloc(sizeof(FunctionCache));
  cache->springs = calloc(size, sizeof(Springs));
  cache->code = calloc(size, sizeof(VerificationCode));
  cache->result = calloc(size, sizeof(long));
  cache->size = 0;
  return cache;
}

void first_part(FILE *input) {
  long sum = 0;
  while (fgets(input_buffer, sizeof(input_buffer), input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    FunctionCache *cache = FunctionCache_init(32768);
    int pos = strcspn(input_buffer, " ");
    input_buffer[pos] = 0;
    Springs springs = Springs_parse(input_buffer);
    VerificationCode code = VerificationCode_parse(input_buffer + pos + 1);
    long n_combinations = 1 << springs.n_unknown;
    sum += count_arangements(springs, code, cache);
  }
  printf("%ld\n", sum);
}

Springs Springs_parse_folded(char *input) {
  Springs springs = {0};
  int input_strlen = strnlen(input, sizeof(springs.layout));
  for (int i = 0; i < 5; i++) {
    for (int j = 0; j < input_strlen; j++) {
      assert(input[j] != 0);
      springs.layout[springs.size] = input[j];
      springs.size++;
    }
    if (i != 4) {
      springs.layout[springs.size] = '?';
      springs.size++;
    }
  }
  for (int i = 0; i < springs.size; i++) {
    if (springs.layout[i] == '?') {
      springs.unknown_spots[springs.n_unknown] = i;
      springs.n_unknown++;
    }
  }
  return springs;
}

VerificationCode VerificationCode_parse_folded(char *input) {
  VerificationCode code = {0};
  for (int i = 0; i < 5; i++) {
    char input_copied[MAX_NUMS];
    memcpy(input_copied, input, strlen(input));
    char *split = strtok(input_copied, ",");
    while (split != NULL) {
      code.numbers[code.size] = strtol(split, NULL, 10);
      code.size++;
      split = strtok(NULL, ",");
    }
  }
  return code;
}

void second_part(FILE *input) {
  long sum = 0;
  int n_line = 0;
  while (fgets(input_buffer, sizeof(input_buffer), input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    FunctionCache *cache = FunctionCache_init(32768);
    int pos = strcspn(input_buffer, " ");
    input_buffer[pos] = 0;
    Springs springs = Springs_parse_folded(input_buffer);
    VerificationCode code =
        VerificationCode_parse_folded(input_buffer + pos + 1);
    long n_combinations = 1 << springs.n_unknown;
    sum += count_arangements(springs, code, cache);
    n_line++;
  }
  printf("%ld\n", sum);
}
