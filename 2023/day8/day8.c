#include "../utils.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>
#define KEYMAXLEN 20
#define MAPSIZE 1000
#define BUFLEN 512

void first_part(FILE *input);
void second_part(FILE *input);

char input_buffer[BUFLEN];

typedef struct Node Node;

struct Node {
  char tag[KEYMAXLEN];
  int index;
  int left;
  int right;
};

typedef struct {
  Node nodes[MAPSIZE];
  int size;
} Nodes;

int Nodes_index_of(Nodes *nodes, char *tag_name) {
  for (int i = 0; i < nodes->size; i++) {
    if (strcmp(nodes->nodes[i].tag, tag_name) == 0) {
      return i;
    }
  }
  return -1;
}

int Nodes_add_tag(Nodes *nodes, char *tag_name) {
  int tag_index = Nodes_index_of(nodes, tag_name);
  if (tag_index >= 0) {
    return tag_index;
  }
  Node node;
  memset(&node, 0, sizeof(Node));
  strncpy(node.tag, tag_name, KEYMAXLEN);
  node.index = nodes->size;
  nodes->nodes[nodes->size] = node;
  nodes->size++;
  return node.index;
}

void Nodes_connect(Nodes *nodes, char *tag_name, char *left, char *right) {
  int tag = Nodes_add_tag(nodes, tag_name);
  int index_left = Nodes_add_tag(nodes, left);
  int index_right = Nodes_add_tag(nodes, right);

  nodes->nodes[tag].left = index_left;
  nodes->nodes[tag].right = index_right;
}

void Nodes_process_line(Nodes *nodes, char *line) {
  char tag[KEYMAXLEN], left[KEYMAXLEN], right[KEYMAXLEN];
  char delim[] = " (),=";
  char *split = strtok(line, delim);
  int part_number = 0;
  char *current_tag;
  while (split != NULL) {
    switch (part_number) {
    case 0:
      current_tag = tag;
      break;
    case 1:
      current_tag = left;
      break;
    default:
      current_tag = right;
      break;
    }
    part_number++;
    strncpy(current_tag, split, KEYMAXLEN);
    split = strtok(NULL, delim);
  }
  Nodes_connect(nodes, tag, left, right);
}

int main(int argc, char *argv[]) {
  process_input(argc, argv, first_part, second_part);
}

void repeat_steps_n_times(Nodes *nodes, char *steps, long *stepcount,
                          Node *next_nodes, int repeats) {
  for (int i = 0; i < nodes->size; i++) {
    int count = 0;
    Node curr = nodes->nodes[i];
    for (int j = 0; j < repeats; j++) {
      for (int k = 0; k < strlen(steps); k++) {
        if (strcmp(curr.tag, "ZZZ") == 0) {
          break;
        }
        count++;
        switch (steps[k]) {
        case 'L':
          curr = nodes->nodes[curr.left];
          break;
        case 'R':
          curr = nodes->nodes[curr.right];
          break;
        }
      }
    }
    stepcount[i] = count;
    next_nodes[i] = curr;
  }
}

long resolve_steps(Nodes *nodes, char *steps) {
  Node curr = nodes->nodes[Nodes_index_of(nodes, "AAA")];
  long count = 0;
  long n_step_result[MAPSIZE] = {0};
  Node next_nodes[MAPSIZE] = {0};

  const int n_repeats = 1;
  repeat_steps_n_times(nodes, steps, n_step_result, next_nodes, n_repeats);

  while (1) {
    if (strcmp(curr.tag, "ZZZ") == 0) {
      return count;
    }
    count += n_step_result[curr.index];
    curr = next_nodes[curr.index];
  }
}

void first_part(FILE *input) {
  int line_number = 0;
  char steps[BUFLEN] = {0};
  char *split;
  Nodes nodes;
  memset(&nodes, 0, sizeof(Nodes));

  while (fgets(input_buffer, BUFLEN, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    if (line_number == 0) {
      strcpy(steps, input_buffer);
    } else if (line_number > 1) {
      Nodes_process_line(&nodes, input_buffer);
    }
    line_number++;
  }

  long n_steps = resolve_steps(&nodes, steps);
  printf("%ld\n", n_steps);
}

void Nodes_select_starting(Nodes *nodes, Nodes *node_buf) {
  for (int i = 0; i < nodes->size; i++) {
    if (nodes->nodes[i].tag[2] == 'A') {
      node_buf->nodes[node_buf->size] = nodes->nodes[i];
      node_buf->size++;
    }
  }
}

void Nodes_get_steps_to_end(Nodes *nodes, Nodes *starting_nodes, char *steps,
                            int *buf) {
  for (int i = 0; i < starting_nodes->size; i++) {
    int count = 0;
    Node curr = starting_nodes->nodes[i];
    while (1) {
      if (curr.tag[2] == 'Z') {
        break;
      }
      for (int k = 0; k < strlen(steps); k++) {
        count++;
        switch (steps[k]) {
        case 'L':
          for (int i = 0; i < starting_nodes->size; i++) {
            curr = nodes->nodes[curr.left];
          }
          break;
        case 'R':
          for (int i = 0; i < starting_nodes->size; i++) {
            curr = nodes->nodes[curr.right];
          }
          break;
        }
      }
    }
    buf[i] = count;
  }
}

unsigned long gcd(unsigned long a, unsigned long b) {
  if (b == 0) {
    return a;
  }
  return gcd(b, a % b);
}

unsigned long lcm(unsigned long a, unsigned long b) {
  if (a > b) {
    return (a / gcd(a, b)) * b;
  } else {
    return (b / gcd(a, b)) * a;
  }
}

long resolve_steps_multiple_starts(Nodes *nodes, char *steps) {
  Node next_nodes[MAPSIZE] = {0};
  Nodes starting_nodes;
  memset(&starting_nodes, 0, sizeof(starting_nodes));
  Nodes_select_starting(nodes, &starting_nodes);

  int steps_to_closest[MAPSIZE] = {0};
  Nodes_get_steps_to_end(nodes, &starting_nodes, steps, steps_to_closest);

  unsigned long prod = strlen(steps);
  for (int i = 0; i < starting_nodes.size; i++) {
    prod = lcm(prod, steps_to_closest[i]);
  }
  return prod;
}

void second_part(FILE *input) {
  int line_number = 0;
  char steps[BUFLEN] = {0};
  char *split;
  Nodes nodes;
  memset(&nodes, 0, sizeof(Nodes));

  while (fgets(input_buffer, BUFLEN, input)) {
    input_buffer[strcspn(input_buffer, "\n")] = 0;
    if (line_number == 0) {
      strcpy(steps, input_buffer);
    } else if (line_number > 1) {
      Nodes_process_line(&nodes, input_buffer);
    }
    line_number++;
  }

  long n_steps = resolve_steps_multiple_starts(&nodes, steps);
  printf("%ld\n", n_steps);
}
