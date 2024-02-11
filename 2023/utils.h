#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int process_input(int argc, char **argv, void (*first_part)(FILE *),
                  void (*second_part)(FILE *)) {
  if (argc != 3) {
    fprintf(stderr,
            "Accepts two command line parameter: task part and input file.\n");
    return EXIT_FAILURE;
  }

  FILE *input = fopen(argv[2], "r");

  if (input == NULL) {
    fprintf(stderr, "Error while opening the file: %s\n", strerror(errno));
    return EXIT_FAILURE;
  }

  switch (atoi(argv[1])) {
  case 1:
    first_part(input);
    break;
  case 2:
    second_part(input);
    break;
  default:
    fprintf(stderr, "Invalid part of task\n");
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}
