#include "../structs/fixed_array.h"
#include "../utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_BUF_IN 256
#define MAX_MODULE_N 100
#define MAX_MODULE_CONNECTED 10
#define MAX_NAME_LEN 20
#define N_REPEATS 1000

void first_part(FILE *input);
void second_part(FILE *input);

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}

typedef char byte;

typedef struct Module Module;

typedef enum {
  TYPE_BUTTON = '*',
  TYPE_BROADCAST = '#',
  TYPE_FLIP_FLOP = '%',
  TYPE_CONJUCTION = '&'
} ModuleType;

typedef struct {
  int items[MAX_MODULE_CONNECTED];
  size_t size;
} ModuleConnectors;

struct Module {
  ModuleType type;
  ModuleConnectors inputs;
  ModuleConnectors outputs;
  int module_position;
};

typedef struct {
  Module items[MAX_MODULE_N];
  size_t size;
} ModuleList;

typedef struct {
  char name[MAX_NAME_LEN];
  int output;
  ModuleConnectors internal;
} ModuleState;

int ModuleState_equals(ModuleState *n1, ModuleState *n2) {
  return strcmp(n1->name, n2->name) == 0;
}

typedef struct {
  ModuleState items[MAX_MODULE_N];
  size_t size;
} State;

void Module_parse(char *line, ModuleList *list, State *outputs) {
  Module *module = NULL;
  char delimiters[] = " ->,\n";
  char *split = strtok(line, delimiters);
  int part = 0;
  while (split != NULL) {
    ModuleState dummy_state = {0};
    Module dummy_module = {0};
    strcpy(dummy_state.name, split + (split[0] == '%') + (split[0] == '&'));
    int index;
    fixed_array_index_of(outputs, &dummy_state, ModuleState_equals, &index);
    if (index < 0) {
      index = outputs->size;
      fixed_array_append(outputs, dummy_state);
      dummy_module.module_position = index;
      fixed_array_append(list, dummy_module);
    }
    Module *current = &list->items[index];

    if (part == 0) {
      module = current;
      switch (split[0]) {
      case '%':
        module->type = split[0];
        split++;
        break;
      case '&':
        module->type = split[0];
        split++;
        break;
      default:
        switch (split[1]) {
        case 'r': // Broadcaster
          module->type = TYPE_BROADCAST;
          break;
        case 'u':
          module->type = TYPE_BUTTON;
          break;
        }
        break;
      }
    } else {
      fixed_array_append(&module->outputs, current->module_position);
      fixed_array_append(&current->inputs, module->module_position);
    }

    split = strtok(NULL, delimiters);
    part++;
  }
}

char input_buf[MAX_BUF_IN];

void first_part(FILE *input) {
  ModuleList *all_modules = calloc(1, sizeof(ModuleList));
  State *module_states = calloc(1, sizeof(State));
  strcpy(input_buf, "button -> broadcaster");

  do {
    Module_parse(input_buf, all_modules, module_states);
  } while (fgets(input_buf, sizeof(input_buf), input));

  for (int i = 0; i < module_states->size; i++) {
    ModuleType type = all_modules->items[i].type;
    module_states->items[i].internal.size =
        (type == TYPE_CONJUCTION) ? all_modules->items[i].inputs.size : 1;
  }

  for (int i = 0; i < all_modules->size; i++) {
    printf("%s\n\tInputs: { ", module_states->items[i].name);
    for (int j = 0; j < all_modules->items[i].inputs.size; j++) {
      printf("%s ",
             module_states->items[all_modules->items[i].inputs.items[j]].name);
    }
    printf("}\n\tOutputs: { ");
    for (int j = 0; j < all_modules->items[i].outputs.size; j++) {
      printf("%s ",
             module_states->items[all_modules->items[i].outputs.items[j]].name);
    }
    printf("}\n");
  }
}

void second_part(FILE *input) {}
