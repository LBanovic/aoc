#include "../utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define N_CARDS 13
#define CARDS_IN_HAND 5
#define NUMBER_OF_HANDS 2000
#define BUF_SIZE 20

char input_buffer[BUF_SIZE];

void first_part(FILE *input);
void second_part(FILE *input);

char card_to_index[] = {['2'] = 0,  ['3'] = 1,  ['4'] = 2, ['5'] = 3, ['6'] = 4,
                        ['7'] = 5,  ['8'] = 6,  ['9'] = 7, ['T'] = 8, ['J'] = 9,
                        ['Q'] = 10, ['K'] = 11, ['A'] = 12};

typedef enum {
  HIGH_CARD,
  ONE_PAIR,
  TWO_PAIR,
  THREE_OF_A_KIND,
  FULL_HOUSE,
  FOUR_OF_A_KIND,
  FIVE_OF_A_KIND,
} HandStrength;

char *hand_strengths[] = {"HIGH_CARD",       "ONE_PAIR",   "TWO_PAIR",
                          "THREE_OF_A_KIND", "FULL_HOUSE", "FOUR_OF_A_KIND",
                          "FIVE_OF_A_KIND"};

typedef struct {
  char content[CARDS_IN_HAND + 1];
  HandStrength strength;
  long bid;
} Hand;

Hand Hand_init() {
  Hand hand;
  memset(&hand, 0, sizeof(Hand));
  return hand;
}

int compare_int_reverse(const void *x, const void *y) {
  int x_i = *(int *)x;
  int y_i = *(int *)y;
  if (x_i < y_i) {
    return 1;
  } else if (x_i > y_i) {
    return -1;
  } else {
    return 0;
  }
}

void Hand_load(Hand *hand, char *line) {
  char *split = strtok(input_buffer, " ");
  int part = 0;
  int numbered_content[N_CARDS] = {0};
  while (split != NULL) {
    if (part == 0) {
      for (int i = 0; i < CARDS_IN_HAND; i++) {
        numbered_content[card_to_index[split[i]]]++;
      }
      qsort(numbered_content, N_CARDS, sizeof(int), compare_int_reverse);
      HandStrength strength = HIGH_CARD;
      for (int i = 0; i < CARDS_IN_HAND; i++) {
        switch (numbered_content[i]) {
        case 5:
          strength = FIVE_OF_A_KIND;
          break;
        case 4:
          strength = FOUR_OF_A_KIND;
          break;
        case 3:
          strength = THREE_OF_A_KIND;
          break;
        case 2:
          switch (strength) {
          case THREE_OF_A_KIND:
            strength = FULL_HOUSE;
            break;
          case ONE_PAIR:
            strength = TWO_PAIR;
            break;
          case HIGH_CARD:
            strength = ONE_PAIR;
            break;
          default:
            break;
          }
        default:
          break;
        }
      }

      memcpy(&hand->content, split, CARDS_IN_HAND + 1);
      hand->strength = strength;
      part++;
    } else {
      hand->bid = strtol(split, NULL, 10);
    }
    split = strtok(NULL, " ");
  }
}

Hand hands[NUMBER_OF_HANDS] = {0};
HandStrength strengths[NUMBER_OF_HANDS] = {0};
int hand_count = 0;

int main(int argc, char *argv[]) {
  return process_input(argc, argv, first_part, second_part);
}

int hand_comparison(const void *hand1, const void *hand2) {
  Hand *h1 = (Hand *)hand1;
  Hand *h2 = (Hand *)hand2;

  if (h1->strength > h2->strength) {
    return 1;
  }

  if (h1->strength < h2->strength) {
    return -1;
  }

  for (int i = 0; i < CARDS_IN_HAND; i++) {
    int index1 = card_to_index[h1->content[i]];
    int index2 = card_to_index[h2->content[i]];

    if (index1 < index2) {
      return -1;
    }

    if (index1 > index2) {
      return 1;
    }
  }
  return 0;
}

void first_part(FILE *input) {
  int part;
  while (fgets(input_buffer, BUF_SIZE, input)) {
    Hand hand = Hand_init();
    Hand_load(&hand, input_buffer);
    memcpy(hands + hand_count, &hand, sizeof(hand));
    hand_count++;
  }

  qsort(hands, hand_count, sizeof(Hand), hand_comparison);

  int sum = 0;
  for (int i = 0; i < hand_count; i++) {
    Hand hand = hands[i];
    sum += hand.bid * (i + 1);
  }
  printf("%d\n", sum);
}
char card_to_index_joker[] = {
    ['J'] = 0,  ['2'] = 1,  ['3'] = 2, ['4'] = 3, ['5'] = 4,
    ['6'] = 5,  ['7'] = 6,  ['8'] = 7, ['9'] = 8, ['T'] = 9,
    ['Q'] = 10, ['K'] = 11, ['A'] = 12};

#define max(a, b) ((a) >= (b) ? (a) : (b))

void Hand_load_joker(Hand *hand, char *line) {
  char *split = strtok(input_buffer, " ");
  int part = 0;
  int numbered_content[N_CARDS] = {0};
  while (split != NULL) {
    if (part == 0) {
      for (int i = 0; i < CARDS_IN_HAND; i++) {
        numbered_content[card_to_index_joker[split[i]]]++;
      }
      int n_jokers = numbered_content[card_to_index_joker['J']];
      numbered_content[card_to_index_joker['J']] = 0;
      qsort(numbered_content, N_CARDS, sizeof(int), compare_int_reverse);
      HandStrength strength = HIGH_CARD;
      for (int i = 0; i < CARDS_IN_HAND; i++) {
        switch (numbered_content[i] + n_jokers) {
        case 5:
          strength = max(FIVE_OF_A_KIND, strength);
          break;
        case 4:
          strength = max(FOUR_OF_A_KIND, strength);
          break;
        case 3:
          strength = max(THREE_OF_A_KIND, strength);
          break;
        case 2:
          switch (strength) {
          case THREE_OF_A_KIND:
            strength = max(FULL_HOUSE, strength);
            break;
          case ONE_PAIR:
            strength = max(TWO_PAIR, strength);
            break;
          case HIGH_CARD:
            strength = max(ONE_PAIR, strength);
            break;
          default:
            break;
          }
        default:
          break;
        }
        n_jokers = 0;
      }

      memcpy(&hand->content, split, CARDS_IN_HAND + 1);
      hand->strength = strength;
      part++;
    } else {
      hand->bid = strtol(split, NULL, 10);
    }
    split = strtok(NULL, " ");
  }
}

int hand_comparison_joker(const void *hand1, const void *hand2) {
  Hand *h1 = (Hand *)hand1;
  Hand *h2 = (Hand *)hand2;

  if (h1->strength > h2->strength) {
    return 1;
  }

  if (h1->strength < h2->strength) {
    return -1;
  }

  for (int i = 0; i < CARDS_IN_HAND; i++) {
    int index1 = card_to_index_joker[h1->content[i]];
    int index2 = card_to_index_joker[h2->content[i]];

    if (index1 < index2) {
      return -1;
    }

    if (index1 > index2) {
      return 1;
    }
  }
  return 0;
}

void second_part(FILE *input) {
  int part;
  while (fgets(input_buffer, BUF_SIZE, input)) {
    Hand hand = Hand_init();
    Hand_load_joker(&hand, input_buffer);
    memcpy(hands + hand_count, &hand, sizeof(hand));
    hand_count++;
  }

  qsort(hands, hand_count, sizeof(Hand), hand_comparison_joker);

  long sum = 0;
  for (int i = 0; i < hand_count; i++) {
    Hand hand = hands[i];
    sum += hand.bid * (i + 1);
  }
  printf("%ld\n", sum);
}
