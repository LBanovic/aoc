#include "../utils.h"
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define PART_FIELD_SIZE 7
#define INPUT_BUFFER_SIZE 512
#define FIELD_MIN 1
#define FIELD_MAX 4000

typedef int elemtype;

typedef struct {
  // Place to store values of 'x', 'm', 'a' and 's'.
  // 7 is the smallest number k where indices for all these letters
  // are different when calculated as (letter - 'a') % 7
  elemtype parts[PART_FIELD_SIZE];
} Part;

int Part_index_of(char field) { return (field - 'a') % PART_FIELD_SIZE; }

elemtype Part_get(Part *p, char field) {
  return p->parts[Part_index_of(field)];
}

void Part_set(Part *p, char field, elemtype value) {
  p->parts[Part_index_of(field)] = value;
}

Part Part_parse(char *line) {
  char delimiters[] = "xmas={},";
  Part p = {0};
  char fields[] = "xmas";
  for (int i = 0; i < strlen(fields); i++) {
    char *split = strtok(i == 0 ? line : NULL, delimiters);
    Part_set(&p, fields[i], strtol(split, NULL, 10));
  }
  return p;
}

#define WORKFLOW_NAME_LENGTH 3
#define MAX_CONDITIONS 10

typedef struct {
  char field;
  elemtype number;
  int less_than;
  char result[WORKFLOW_NAME_LENGTH + 1];
} Condition;

Condition Condition_parse(char *line) {
  char *saveptr;
  char delimiters[] = ":\n";
  char *split = strtok_r(line, delimiters, &saveptr);
  Condition c = {0};
  while (split != NULL) {
    switch (split[1]) {
    case '<':
    case '>':
      c.field = split[0];
      c.less_than = split[1] == '<';
      c.number = strtol(split + 2, NULL, 10);
      break;
    default:
      strncpy(c.result, split, sizeof(c.result));
      break;
    }
    split = strtok_r(NULL, delimiters, &saveptr);
  }
  return c;
}

char *Condition_satisfied(Part *p, Condition *condition) {
  if (condition->field == 0) {
    return condition->result;
  }
  elemtype result = Part_get(p, condition->field) - condition->number;
  if (condition->less_than) {
    result *= -1;
  }
  if (result > 0) {
    return condition->result;
  }
  return NULL;
}

typedef struct {
  char name[WORKFLOW_NAME_LENGTH + 1];
  Condition conditions[MAX_CONDITIONS];
  size_t size;
} Workflow;

void Workflow_add_condition(Workflow *workflow, Condition condition) {
  workflow->conditions[workflow->size] = condition;
  workflow->size++;
}

char *Workflow_run(Workflow *workflow, Part part) {
  for (int i = 0; i < workflow->size; i++) {
    char *condition_result =
        Condition_satisfied(&part, &workflow->conditions[i]);
    if (condition_result != NULL) {
      return condition_result;
    }
  }
  return NULL;
}

Workflow Workflow_parse(char *line) {
  Workflow workflow = {0};
  int part = 0;
  char delimiters[] = "{},\n";
  char *saveptr;
  char *split = strtok_r(line, delimiters, &saveptr);
  while (split != NULL) {
    if (part == 0) {
      strncpy(workflow.name, split, WORKFLOW_NAME_LENGTH);
    } else {
      Condition condition = Condition_parse(split);
      Workflow_add_condition(&workflow, condition);
    }
    part++;
    split = strtok_r(NULL, delimiters, &saveptr);
  }
  return workflow;
}

#define ALPHABET_SIZE 26

typedef struct {
  // +1 to allow for workflow names of length 2
  Workflow workflows[ALPHABET_SIZE][ALPHABET_SIZE][ALPHABET_SIZE + 1];
  size_t size;
} WorkflowMap;

Workflow WorkflowMap_get(WorkflowMap *map, char *name) {
  if (!(strlen(name) == WORKFLOW_NAME_LENGTH ||
        strlen(name) == WORKFLOW_NAME_LENGTH - 1)) {
    fprintf(stderr, "string: %s\n", name);
    assert(0);
  }
  int first_index = name[0] - 'a';
  int second_index = name[1] - 'a';
  // if name is 2 characters long, the last index should be 0.
  int third_index = name[2] - 'a' + 1;
  if (name[2] == 0) {
    third_index = 0;
  }
  return map->workflows[first_index][second_index][third_index];
}

void WorkflowMap_add(WorkflowMap *map, Workflow workflow) {
  int first_index = workflow.name[0] - 'a';
  int second_index = workflow.name[1] - 'a';
  int third_index = workflow.name[2] == 0 ? 0 : workflow.name[2] - 'a' + 1;
  map->workflows[first_index][second_index][third_index] = workflow;
  map->size++;
}

char input_buffer[INPUT_BUFFER_SIZE] = {0};

void first_part(FILE *input) {
  int parse_parts = 0;
  WorkflowMap map = {0};
  int sum = 0;
  while (fgets(input_buffer, sizeof(input_buffer), input)) {
    if (input_buffer[0] == '\n') {
      parse_parts = 1;
      continue;
    }
    if (!parse_parts) {
      Workflow workflow = Workflow_parse(input_buffer);
      WorkflowMap_add(&map, workflow);
    }
    if (parse_parts) {
      Part part = Part_parse(input_buffer);
      Workflow current = WorkflowMap_get(&map, "in");
      while (1) {
        char *result = Workflow_run(&current, part);
        if (result[0] == 'A') {
          for (int i = 0; i < sizeof(part.parts) / sizeof(part.parts[0]); i++) {
            sum += part.parts[i];
          }
          break;
        } else if (result[0] == 'R') {
          break;
        }
        current = WorkflowMap_get(&map, result);
      }
    }
  }
  printf("%d\n", sum);
}

typedef struct {
  // 7 elements like in Part struct
  elemtype min[PART_FIELD_SIZE];
  elemtype max[PART_FIELD_SIZE];
} Interval;

int Interval_index_of(char field) { return (field - 'a') % PART_FIELD_SIZE; }

elemtype Interval_get_min(const Interval *interval, const char field) {
  return interval->min[Interval_index_of(field)];
}

elemtype Interval_get_max(const Interval *interval, const char field) {
  return interval->max[Interval_index_of(field)];
}

void Interval_set_min(Interval *interval, char field, elemtype value) {
  interval->min[Interval_index_of(field)] = value;
}

void Interval_set_max(Interval *interval, char field, elemtype value) {
  interval->max[Interval_index_of(field)] = value;
}

long Interval_get_prod(Interval *interval) {
  char fields[] = "xmas";
  long prod = 1;
  for (int i = 0; i < 4; i++) {
    prod *= (Interval_get_max(interval, fields[i]) -
             Interval_get_min(interval, fields[i]) + 1);
  }
  return prod;
}

Interval Interval_default(void) {
  Interval interval = {0};
  char fields[] = "xmas";
  for (int i = 0; i < 4; i++) {
    Interval_set_min(&interval, fields[i], FIELD_MIN);
    Interval_set_max(&interval, fields[i], FIELD_MAX);
  }
  return interval;
}

#define MAX_INTERVALS 100000

typedef struct {
  Interval elements[MAX_INTERVALS];
  char workflow_names[MAX_INTERVALS][WORKFLOW_NAME_LENGTH + 1];
  size_t size;
} List;

void List_pop(List *list, Interval *interval, char *result) {
  *interval = list->elements[0];
  strncpy(result, list->workflow_names[0], sizeof(list->workflow_names[0]));
  memmove(list->elements, list->elements + 1,
          sizeof(Interval) * (list->size - 1));
  memmove(list->workflow_names, list->workflow_names + 1,
          sizeof(list->workflow_names[0]) * (list->size - 1));
  list->size--;
}

void List_add(List *list, Interval interval, char *workflow_name) {
  list->elements[list->size] = interval;
  strncpy(list->workflow_names[list->size], workflow_name,
          sizeof(list->workflow_names[list->size]));
  list->size++;
}

void List_extend(List *original, List *extender) {
  Interval extended;
  char workflow_name[WORKFLOW_NAME_LENGTH + 1];

  while (extender->size > 0) {
    List_pop(extender, &extended, workflow_name);
    List_add(original, extended, workflow_name);
  }
}

List *Workflow_apply_list(Workflow *workflow, Interval interval,
                          List *outlist) {
  for (int i = 0; i < workflow->size - 1; i++) {
    Interval one_side = interval;
    Interval other_side = interval;
    Condition c = workflow->conditions[i];
    if (c.less_than) {
      Interval_set_max(&one_side, c.field, c.number - 1);
      Interval_set_min(&other_side, c.field, c.number);
    } else {
      Interval_set_min(&one_side, c.field, c.number + 1);
      Interval_set_max(&other_side, c.field, c.number);
    }
    List_add(outlist, one_side, c.result);
    interval = other_side;
  }
  List_add(outlist, interval, workflow->conditions[workflow->size - 1].result);
  return outlist;
}

void second_part(FILE *input) {
  WorkflowMap map = {0};

  while (fgets(input_buffer, sizeof(input_buffer), input)) {
    if (input_buffer[0] == '\n') {
      break;
    }
    Workflow workflow = Workflow_parse(input_buffer);
    WorkflowMap_add(&map, workflow);
  }
  List *intervals = calloc(1, sizeof(List));
  Interval current = Interval_default();
  char workflow_name[WORKFLOW_NAME_LENGTH + 1] = "in";
  List_add(intervals, current, workflow_name);

  List *outlist = calloc(1, sizeof(List));

  long sum = 0;
  while (intervals->size > 0) {
    List_pop(intervals, &current, workflow_name);
    if (workflow_name[0] == 'A') {
      long prod = Interval_get_prod(&current);
      sum += prod;
      continue;
    }
    if (workflow_name[0] == 'R') {
      long prod = Interval_get_prod(&current);
      continue;
    }
    Workflow workflow = WorkflowMap_get(&map, workflow_name);
    Workflow_apply_list(&workflow, current, outlist);
    List_extend(intervals, outlist);
  }
  printf("%ld\n", sum);
}

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}
