#include "../structs/fixed_array.h"
#include "../utils.h"
#include <complex.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_N_ELEMENTS 150

typedef struct {
  int elements[MAX_N_ELEMENTS][MAX_N_ELEMENTS];
  size_t n_rows;
  size_t n_cols;
} Map;

Map Map_parse(FILE *input) {
  char c;
  Map map = {0};
  int row_len = 0;
  while ((c = fgetc(input)) != EOF) {
    if (c == '\n') {
      if (map.n_cols == 0) {
        map.n_cols = row_len;
      }
      row_len = 0;
      map.n_rows++;
    } else {
      map.elements[map.n_rows][row_len] = c - '0';
      row_len++;
    }
  }
  return map;
}

typedef struct {
  int i;
  int j;
  complex double direction;
  int weight;
} State;

State State_next(State state, Map *map) {
  state.i += cimag(state.direction);
  state.j += creal(state.direction);
  state.weight += map->elements[state.i][state.j];
  return state;
}

State State_turn_left(State state) {
  state.direction *= -I;
  return state;
}

State State_turn_right(State state) {
  state.direction *= I;
  return state;
}

#define MAX_LIST_SIZE 1000000
typedef struct {
  State items[MAX_LIST_SIZE];
  size_t size;
} List;

void List_add(List *list, State state) { fixed_array_append(list, state); }

State List_pop_min(List *list) {
  int min_index = 0;
  for (int i = 1; i < list->size; i++) {
    if (list->items[i].weight < list->items[min_index].weight) {
      min_index = i;
    }
  }
  State min_state;
  fixed_array_pop(list, min_index, &min_state);
  return min_state;
}

int State_equals(State *s1, State *s2) {
  return s1->i == s2->i && s1->j == s2->j && s1->direction == s2->direction;
}

int List_is_in(List *list, State state) {
  int retval;
  fixed_array_index_of(list, &state, State_equals, &retval);
  return retval >= 0;
}

void first_part(FILE *input) {
  Map map = Map_parse(input);
  List *seen = calloc(1, sizeof(List));
  List *candidates = calloc(1, sizeof(List));

  State s1 = {0, 0, 1, 0};
  List_add(candidates, s1);
  State s2 = {0, 0, I, 0};
  List_add(candidates, s2);

  State current;
  while (1) {
    current = List_pop_min(candidates);
    if (current.i == map.n_rows - 1 && current.j == map.n_cols - 1) {
      break;
    }
    if (List_is_in(seen, current)) {
      continue;
    }
    List_add(seen, current);

    State left = State_turn_left(current);
    for (int i = 0; i < 3; i++) {
      State step = State_next(left, &map);
      if (step.i >= 0 && step.i < map.n_rows && step.j >= 0 &&
          step.j < map.n_cols) {
        List_add(candidates, step);
      }
      left = step;
    }

    State right = State_turn_right(current);
    for (int i = 0; i < 3; i++) {
      State step = State_next(right, &map);
      if (step.i >= 0 && step.i < map.n_rows && step.j >= 0 &&
          step.j < map.n_cols) {
        List_add(candidates, step);
      }
      right = step;
    }
  }
  printf("%d\n", current.weight);
}

void second_part(FILE *input) {
  Map map = Map_parse(input);
  List *seen = calloc(1, sizeof(List));
  List *candidates = calloc(1, sizeof(List));

  State s1 = {0, 0, 1, 0};
  List_add(candidates, s1);
  State s2 = {0, 0, I, 0};
  List_add(candidates, s2);

  State current;
  while (1) {
    current = List_pop_min(candidates);
    if (current.i == map.n_rows - 1 && current.j == map.n_cols - 1) {
      break;
    }
    if (List_is_in(seen, current)) {
      continue;
    }
    List_add(seen, current);

    State left = State_turn_left(current);
    for (int i = 0; i < 10; i++) {
      State step = State_next(left, &map);
      if (step.i >= 0 && step.i < map.n_rows && step.j >= 0 &&
          step.j < map.n_cols && i >= 3) {
        List_add(candidates, step);
      }
      left = step;
    }

    State right = State_turn_right(current);
    for (int i = 0; i < 10; i++) {
      State step = State_next(right, &map);
      if (step.i >= 0 && step.i < map.n_rows && step.j >= 0 &&
          step.j < map.n_cols && i >= 3) {
        List_add(candidates, step);
      }
      right = step;
    }
  }
  printf("%d\n", current.weight);
}

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}
